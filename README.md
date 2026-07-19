# Eco-Grid Backend (Django)

A small, plain Django + Django REST Framework backend for the **bright-wise-control**
frontend. It intentionally only covers 4 things, as requested:

1. **Users** — `users` app
2. **Buildings** — `buildings` app
3. **Brightness / fixture control** — also in the `buildings` app (`Fixture` model)
4. **Analytics** (energy usage/saved/CO₂) — `analytics` app

Everything else the frontend shows (floors, rooms, zones, automation rules, AI
insights, alerts, reports) is **not** implemented — the frontend keeps using its
mock data (`src/mocks/data.ts`) for those pages.

No fancy layers, no extra abstractions — just Django models, DRF serializers,
and DRF viewsets, so it's easy to read top to bottom.

## Project layout

```
ecogrid_backend/
├── ecogrid/          # project settings + root urls.py
├── users/            # User model (extends Django's built-in user) + login/logout
├── buildings/        # Building + Fixture models, brightness control endpoint
└── analytics/        # EnergyRecord model, summary/trend endpoints
```

## Setup

```bash
cd ecogrid_backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # adjust if needed

python manage.py migrate
python manage.py seed_demo_data # optional: fills in sample buildings/fixtures/users
python manage.py runserver
```

The API is now at `http://localhost:8000/api/`.

`seed_demo_data` also creates a superuser: **admin / admin12345** — you can view
and edit everything at `http://localhost:8000/admin/` too.

## Connecting the frontend

In the frontend's `.env`, set:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

The frontend's `apiClient` (`src/lib/api/client.ts`) reads a token from
`localStorage.getItem("ecogrid_token")` and sends it as
`Authorization: Bearer <token>`. This backend's login endpoint returns that
same kind of token, so no frontend changes are needed — after logging in,
just store the returned `token` in `localStorage` under `ecogrid_token`.

## Endpoints

### Auth
| Method | URL | Notes |
|---|---|---|
| POST | `/api/auth/login/` | `{ "username": "admin", "password": "admin12345" }` → `{ token, user }` |
| POST | `/api/auth/logout/` | Deletes the current token |

### Users
| Method | URL | Notes |
|---|---|---|
| GET | `/api/users/` | List all users |
| POST | `/api/users/` | Create/invite a user (needs `password`) |
| GET | `/api/users/{id}/` | User detail |
| PATCH | `/api/users/{id}/` | Update role, building, active status, etc. |
| DELETE | `/api/users/{id}/` | Remove user |
| GET | `/api/users/me/` | The logged-in user's own profile |

### Buildings
| Method | URL | Notes |
|---|---|---|
| GET | `/api/buildings/` | List buildings (with live fixture count + energy usage) |
| POST | `/api/buildings/` | Create a building |
| GET/PATCH/DELETE | `/api/buildings/{id}/` | Detail / update / delete |

### Fixtures & brightness control
| Method | URL | Notes |
|---|---|---|
| GET | `/api/fixtures/?building={id}` | List fixtures, optionally by building |
| POST | `/api/fixtures/` | Create a fixture |
| GET/PATCH/DELETE | `/api/fixtures/{id}/` | Detail / update / delete |
| **PATCH** | **`/api/fixtures/{id}/control/`** | **The brightness/on-off endpoint** — body: `{ "is_on": true, "brightness": 70 }` |
| POST | `/api/fixtures/bulk_control/` | Turn all (or one building's) online fixtures on/off — body: `{ "is_on": true, "building": 1 }` |

### Analytics
| Method | URL | Notes |
|---|---|---|
| GET | `/api/analytics/summary/` | Totals: buildings, fixtures online/offline, kWh used/saved, CO₂ reduced |
| GET | `/api/analytics/energy/?group=day\|month&building={id}` | Time series for the load/trend charts |
| GET | `/api/analytics/by-building/` | Usage/saved totals per building, for the comparison chart |

## Why these design choices

- **SQLite by default** — zero setup, swap `DATABASES` in `ecogrid/settings.py`
  for Postgres/MySQL later if needed.
- **Token auth, not JWT** — one `Token` model, one `Authorization: Bearer <token>`
  header, easy to reason about. Swap for `djangorestframework-simplejwt` later
  if you need refresh tokens.
- **`EnergyRecord` is one row per building per day** — all the charts (daily,
  monthly, per-building) are computed by summing/grouping that single table in
  the view, instead of maintaining several pre-aggregated tables.
- **`Fixture.brightness` and `Fixture.is_on` are the only two fields the
  `/control/` endpoint accepts** — every other field (power draw, voltage,
  health, firmware) is meant to be reported by the device/gateway, not edited
  by a user, so it's editable only through the normal admin/API update, not
  the control action.
