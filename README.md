## markdown-to-az-resources-json

markdown 형식의 문서, 또는 텍스트 기반의 프로젝트 개요와 리소스 목록을 입력하면
해당 내용을 기반으로 azure resources 를 json 형태로 산출해주는 에이전트

출력 예시
```json
{
  "resources": [
    {
      "type": "aks",
      "name": "aks-az01-prd-diagramagent-01",
      "subnet": "app",
      "nodepools": [
        { "name": "system", "count": 3 },
        { "name": "user", "count": 5 }
      ]
    },
    {
      "type": "paas-mysql",
      "name": "mysql-az01-prd-diagramagent-01"
    },
    {
      "type": "pe",
      "name": "pe-az01-prd-diagramagent-mysql-01",
      "subnet": "pe",
      "origin": "mysql-az01-prd-diagramagent-01"
    }
  ]
}
```
