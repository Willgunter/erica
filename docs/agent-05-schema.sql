create extension if not exists pgcrypto;

create table if not exists public.lesson_summaries (
  id uuid primary key default gen_random_uuid(),
  user_id text not null,
  lesson_id text not null,
  lesson_title text not null,
  created_at timestamptz not null default now(),
  accuracy numeric(5,2) not null default 0,
  correct_count integer not null default 0,
  incorrect_count integer not null default 0,
  topics jsonb not null default '[]'::jsonb,
  focus_areas text[] not null default '{}'::text[],
  recommendations text[] not null default '{}'::text[],
  replay_payload jsonb not null default '{}'::jsonb,
  source_payload jsonb not null default '{}'::jsonb
);

create index if not exists lesson_summaries_user_created_idx
  on public.lesson_summaries (user_id, created_at desc);

create index if not exists lesson_summaries_lesson_idx
  on public.lesson_summaries (lesson_id);

alter table public.lesson_summaries enable row level security;
