# Fintoc CLI — Referencia

Fuente: https://github.com/fintoc-com/fintoc-cli  
Versión: `0.3.0` (early access — commands pueden cambiar)  
Requires: Node.js >= 22

## Instalación

```bash
npm install -g @fintoc/cli
```

## Auth

```bash
fintoc login                          # interactivo
fintoc login --api-key sk_test_...    # no interactivo (CI)
fintoc logout                         # eliminar credenciales
fintoc config show                    # ver config activa
```

**Orden de resolución de API key:**
1. Flag `--api-key` (por comando)
2. `FINTOC_API_KEY` (env var)
3. `~/.fintoc/config.toml`

## Recursos — patrón: `fintoc <resource> <action> [flags]`

| Resource | Actions |
|---|---|
| `payment_intents` | `get`, `list` |
| `charges` | `create`, `get`, `list` |
| `webhook_endpoints` | `create`, `get`, `list`, `delete` |
| `checkout_sessions` | `create`, `get`, `expire` |
| `subscriptions` | `get`, `list` |
| `links` | `get`, `list`, `delete` |
| `api_keys` | `list` |
| `v2 transfers` | `create`, `get`, `list` |
| `v2 accounts` | `get`, `list` |
| `v2 account_verifications` | `create`, `get`, `list` |
| `v2 account_numbers` | `create`, `get`, `list`, `delete` |
| `v2 movements` | `get`, `list` |

## Utilities

```bash
fintoc doctor                   # diagnóstico de setup y conectividad
fintoc open dashboard           # abrir dashboard en browser
fintoc webhooks listen          # escuchar eventos en tiempo real
fintoc trigger <event>          # disparar evento de prueba
```

## Ejemplos

### Listar con filtros

```bash
fintoc charges list --status succeeded --since 2026-01-01 --limit 5
```

### Get por ID

```bash
fintoc payment_intents get pi_test_abc123
```

### Crear con flags

```bash
fintoc charges create --amount 5000 --currency CLP --subscription-id sub_test_abc123
```

### Crear desde JSON

```bash
fintoc charges create --from-json payload.json
cat payload.json | fintoc charges create --from-json -
```

Los flags tienen precedencia sobre el JSON. Arrays se reemplazan completos (no merge).

### Webhook endpoints

```bash
# Crear
fintoc webhook_endpoints create --url https://example.com/hooks --enabled-events payment_intent.succeeded

# Escuchar localmente
fintoc webhooks listen --forward-to http://localhost:3000/webhooks

# Trigger eventos
fintoc trigger payment_intent.succeeded
fintoc trigger payment_intent.succeeded --override amount=5000 --override currency=CLP
fintoc trigger payment_intent.succeeded --override metadata.order_id=abc123
```

### Eliminar con confirmación

```bash
fintoc webhook_endpoints delete we_test_abc123
fintoc webhook_endpoints delete we_test_abc123 --yes   # skip confirm (CI)
```

### Transferencias v2 (requiere JWS)

```bash
fintoc v2 transfers create \
  --amount 10000 \
  --currency CLP \
  --account-id acc_test_abc123 \
  --counterparty-account-number 12345678 \
  --counterparty-institution-id cl_banco_estado \
  --jws-private-key ~/path/to/private_key.pem
```

La JWS key también puede configurarse en `~/.fintoc/config.toml` como `jws_private_key`.

### JSON output (para scripts/CI)

```bash
fintoc payment_intents list --json
fintoc v2 accounts get acc_test_abc123 --json
fintoc charges list --json --no-color | jq '.[] | .id'
```

### Descubrir flags disponibles

```bash
fintoc charges create --help
fintoc v2 transfers list --help
```
