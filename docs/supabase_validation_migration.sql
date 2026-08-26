-- Ground-truth validation persistence for existing Supabase deployments.
-- Safe to run repeatedly in the Supabase SQL editor.
create table if not exists public.validation_runs (
  validation_id text primary key,
  scenario_id text not null,
  provider text not null,
  evidence_class text not null,
  baseline_identity text not null,
  reference_identity text not null,
  configuration jsonb not null default '{}'::jsonb,
  report jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_validation_scenario
  on public.validation_runs (scenario_id, created_at desc);

-- Backend writes use the service-role key. Anonymous browser writes are not
-- permitted; validation endpoints remain server-mediated and read-only to users.
alter table public.validation_runs enable row level security;
