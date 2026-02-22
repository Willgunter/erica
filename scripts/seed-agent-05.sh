#!/usr/bin/env sh

set -eu

BASE_URL="${BASE_URL:-http://localhost:8000}"
USER_ID="${1:-demo-user}"

curl --fail --silent --show-error \
  -X POST "${BASE_URL}/api/summary" \
  -H "Content-Type: application/json" \
  -d "{
    \"userId\": \"${USER_ID}\",
    \"lesson\": {
      \"id\": \"seed-lesson-$(date +%s)\",
      \"title\": \"Functions and Graph Interpretation\",
      \"estimated_duration\": 28,
      \"modules\": [
        {\"id\": \"m-1\", \"title\": \"Domain and Range\", \"core_topics\": [\"Domain/Range\"]},
        {\"id\": \"m-2\", \"title\": \"Slope from Tables\", \"core_topics\": [\"Slope\"]},
        {\"id\": \"m-3\", \"title\": \"Model Comparison\", \"core_topics\": [\"Applications\"]}
      ],
      \"media_assets\": [
        {\"type\": \"video\", \"label\": \"Domain/Range Demo\", \"url\": \"https://example.com/domain-range\"},
        {\"type\": \"audio\", \"label\": \"Slope Recap\", \"url\": \"https://example.com/slope-recap\"}
      ]
    },
    \"test_result\": {
      \"completed\": true,
      \"feedback\": {
        \"strong_topics\": [\"Domain/Range\", \"Slope\"],
        \"focus_topics\": [\"Applications\", \"Slope\"]
      }
    },
    \"checkpoint_sessions\": [
      {
        \"module_id\": \"m-1\",
        \"qa_pairs\": [{\"question\": \"Describe range\", \"answer\": \"Output set\"}]
      },
      {
        \"module_id\": \"m-3\",
        \"qa_pairs\": [{\"question\": \"Choose model\", \"answer\": \"Linear growth\"}]
      }
    ]
  }"

echo
echo "Seed summary created for user '${USER_ID}'"
