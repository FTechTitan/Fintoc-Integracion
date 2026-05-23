# Fintoc — Integración

Repositorio de trabajo para la integración con [Fintoc](https://fintoc.com): documentación de referencia, ejemplos y notas de implementación.

## Recursos oficiales

| Recurso | URL |
|---|---|
| Documentación | https://docs.fintoc.com/docs |
| API Reference | https://docs.fintoc.com/reference/introduction |
| Dashboard | https://dashboard.fintoc.com |
| GitHub Fintoc | https://github.com/fintoc-com |
| Quickstart | https://github.com/fintoc-com/quickstart |

## Fintoc CLI

**Versión instalada:** `0.3.0` (Node.js >= 22 requerido)

### Instalación

```bash
# Requiere Node.js 22+
nvm use 22
npm install -g @fintoc/cli
```

### Autenticación

```bash
fintoc login                        # interactivo
fintoc login --api-key sk_test_...  # no interactivo
fintoc config show                  # ver configuración activa
fintoc doctor                       # diagnóstico de setup
```

El CLI busca la API key en este orden:
1. Flag `--api-key` (por comando)
2. Variable de entorno `FINTOC_API_KEY`
3. `~/.fintoc/config.toml` (guardado con `fintoc login`)

### Recursos disponibles

```
fintoc payment_intents    list | get
fintoc charges            create | get | list
fintoc webhook_endpoints  create | get | list | delete
fintoc checkout_sessions  create | get | expire
fintoc subscriptions      get | list
fintoc links              get | list | delete
fintoc api_keys           list
fintoc v2 transfers       create | get | list
fintoc v2 accounts        get | list
fintoc v2 account_verifications  create | get | list
fintoc v2 account_numbers        create | get | list | delete
fintoc v2 movements       get | list
```

### Utilities

```bash
fintoc doctor                              # verificar setup
fintoc open dashboard                      # abrir dashboard en browser
fintoc webhooks listen                     # escuchar eventos en tiempo real
fintoc webhooks listen --forward-to http://localhost:3000/webhooks
fintoc trigger payment_intent.succeeded    # disparar evento de prueba
```

### Ejemplos de uso

```bash
# Listar con filtros
fintoc charges list --status succeeded --since 2026-01-01 --limit 5

# Crear con flags
fintoc charges create --amount 5000 --currency CLP --subscription-id sub_test_abc123

# Crear desde JSON
cat payload.json | fintoc charges create --from-json -

# Output JSON para scripts
fintoc payment_intents list --json

# Ayuda de cualquier comando
fintoc charges create --help
```

## Estructura del repo

```
.
├── README.md
└── docs/
    ├── overview.md          # Estructura completa de la documentación
    ├── api-keys.md          # API Keys y autenticación
    ├── test-mode.md         # Modo sandbox/test
    └── cli-reference.md     # Referencia completa del CLI
```

## Variables de entorno

```bash
# .env (nunca commitear)
FINTOC_API_KEY=sk_test_...     # Secret key (test o live)
```
