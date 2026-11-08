CREATE TABLE IF NOT EXISTS audit_events (
 id bigserial PRIMARY KEY, actor text NOT NULL, tenant_id text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);

drop table audit_events;