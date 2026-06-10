# HubSpot Deal Webhook Payload Schema

## Key Fields We Use
| Field | Path | Example Value |
|---|---|---|
| Deal Name | properties.dealname.value | "Acme Corp" |
| Deal Stage | properties.dealstage.value | "closedwon" |
| Deal Amount | properties.amount.value | "12000" |
| Close Date | properties.closedate.value | "1750000000000" |
| Deal ID | dealId | 12345678 |

## Trigger Condition
- Field: `dealstage`
- Value that triggers OnboardIQ: `closedwon`