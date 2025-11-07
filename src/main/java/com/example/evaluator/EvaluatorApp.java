package com.example.evaluator;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.kie.api.KieServices;
import org.kie.api.runtime.KieSession;
import org.kie.api.runtime.KieContainer;

import java.io.File;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.logging.Logger;

public class EvaluatorApp {
    private static final Logger logger = Logger.getLogger("EvaluatorApp");

    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("Usage: java -jar evaluator.jar <path-to-json>");
            System.exit(1);
        }

        String jsonPath = args[0];
        ObjectMapper om = new ObjectMapper();
        JsonNode root = om.readTree(new File(jsonPath));

        FunctionalCorrectness fc = new FunctionalCorrectness();
        LinterValidation lv = new LinterValidation();
        GenAiEvaluation ge = new GenAiEvaluation();
        ScoreResult sr = new ScoreResult();

        JsonNode functional = root.path("functional_correctness");
        JsonNode finalReport = functional.path("final_report");
        if (!finalReport.isMissingNode()) {
            fc.setTotalPairs(finalReport.path("total_pairs").asInt(0));
            fc.setGroundedReplies(finalReport.path("grounded_replies").asInt(0));
            fc.setTotalCitations(finalReport.path("total_citations").asInt(0));
            fc.setCorrectCitations(finalReport.path("correct_citations").asInt(0));
            fc.setMissingCitations(finalReport.path("missing_citations").asInt(0));
            fc.setHallucinatedReplies(finalReport.path("hallucinated_replies").asInt(0));
        }

        JsonNode linterArray = root.path("linter_validation");
        if (linterArray.isArray() && linterArray.size() > 0) {
            JsonNode li = linterArray.get(0);
            JsonNode summary = li.path("summary");
            lv.setTotalFiles(summary.path("total_files").asInt(li.path("total_files").asInt(0)));
            lv.setFilesWithErrors(summary.path("files_with_errors").asInt(li.path("files_with_errors").asInt(0)));
            JsonNode pylint = summary.path("pylint");
            int warnings = 0;
            if (!pylint.isMissingNode()) {
                warnings = pylint.path("total_warnings").asInt(pylint.path("warning_count").asInt(0));
            }
            lv.setTotalPylintWarnings(warnings);
        }

        Map<String, String> map = new HashMap<>();
        JsonNode genai = root.path("genai_evaluation");
        JsonNode criteria = genai.path("criteria_evaluations");
        if (criteria.isArray()) {
            for (JsonNode c : criteria) {
                Iterator<String> it = c.fieldNames();
                while (it.hasNext()) {
                    String key = it.next();
                    JsonNode val = c.path(key);
                    String quality = val.path("quality").asText(null);
                    if (quality == null || quality.isEmpty()) quality = "average";
                    map.put(key, quality);
                }
            }
        }
        ge.setCriteriaQuality(map);

        String summary = root.path("summary").asText(null);
        sr.setSummary(summary);

        KieServices ks = KieServices.Factory.get();
        KieContainer kc = ks.getKieClasspathContainer();
        KieSession ksession = kc.newKieSession("ksession-rules");
        ksession.setGlobal("logger", logger);

        ksession.insert(fc);
        ksession.insert(lv);
        ksession.insert(ge);
        ksession.insert(sr);

        int fired = ksession.fireAllRules();
        logger.info("Rules fired: " + fired);

        System.out.println("=== EVALUATION RESULT ===");
        System.out.println("Static score (20%): " + sr.getStaticScore());
        System.out.println("Functional score (30%): " + sr.getFunctionalScore());
        System.out.println("Usecase/GenAI score (50%): " + sr.getUsecaseScore());
        System.out.println("Final score (0-100): " + sr.getFinalScore());
        System.out.println("Summary:");
        System.out.println(sr.getSummary());

        ksession.dispose();
    }
}
