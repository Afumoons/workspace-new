---
name: whatsapp-outbound-webhook
description: Handle inbound HTTP webhook calls to send WhatsApp messages via OpenClaw, secured with a shared token (?token=clio-autotrading-hooks). Use when external systems (e.g., autonomous_trading_ai) need to deliver WhatsApp alerts through a simple POST JSON payload.
---

# WhatsApp Outbound Webhook Skill

This skill exposes an HTTP webhook that other systems can call to send WhatsApp messages through OpenClaw. It is designed to integrate with the `autonomous_trading_ai` project and its `notifications/whatsapp_notifier.py` module.

## Contract

**HTTP endpoint** (example):

- Method: `POST`
- Path: `/hooks/whatsapp_outbound`
- Auth: query parameter `token` must match the shared secret
- Content-Type: `application/json`

### Query Parameters

- `token` (required): shared secret for this deployment.
  - Default: `clio-autotrading-hooks`
  - Can be overridden via environment variable `WEBHOOK_TOKEN`.

### Request Body

JSON object:

```json
{
  "to": "628170090022",
  "message": "text to send"
}
```

- `to` (string, required): recipient number in international format without `+`.
- `message` (string, required): text body to send via WhatsApp.

### Response

- `200 OK` on success, JSON like:

```json
{"status": "ok"}
```

- `400 Bad Request` if body is invalid.
- `401 Unauthorized` if token is missing or incorrect.
- `500 Internal Server Error` for unexpected failures.

## Implementation Notes

- Read `WEBHOOK_TOKEN` from environment, defaulting to `clio-autotrading-hooks`.
- Never log the full token; log only that auth failed.
- Use OpenClaw's messaging tools or existing WhatsApp integration to actually deliver the message.

## Usage from autonomous_trading_ai

In `autonomous_trading_ai`:

- Set `.env`:

```env
OPENCLAW_WHATSAPP_WEBHOOK=https://<openclaw-host>/hooks/whatsapp_outbound
WEBHOOK_TOKEN=clio-autotrading-hooks
```

- `notifications/whatsapp_notifier.py` will automatically append `?token=...` to the webhook URL based on `WEBHOOK_TOKEN`.

## TODO

- Implement the actual HTTP handler in the agent runtime using the above contract.
- Wire it to OpenClaw's underlying WhatsApp send mechanism (e.g., message tool or an existing WhatsApp skill) so that `{ "to", "message" }` gets delivered correctly.
