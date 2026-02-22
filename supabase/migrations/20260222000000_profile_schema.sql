-- Agent 01: onboarding profile schema

create extension if not exists pgcrypto;

create or replace function public.touch_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  subject text not null,
  goals text[] not null default '{}',
  study_time text not null check (study_time in ('15_min', '30_min', '45_min', '60_min_plus')),
  pacing text not null check (pacing in ('light', 'steady', 'accelerated')),
  accessibility jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.learning_preferences (
  user_id uuid primary key references auth.users(id) on delete cascade,
  teaching_style text check (teaching_style in ('visual', 'socratic', 'project_based', 'mixed')),
  content_formats text[] not null default '{}',
  review_preferences text[] not null default '{}',
  uncertainty_flags jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create trigger touch_profiles_updated_at
before update on public.profiles
for each row
execute function public.touch_updated_at();

create trigger touch_learning_preferences_updated_at
before update on public.learning_preferences
for each row
execute function public.touch_updated_at();

alter table public.profiles enable row level security;
alter table public.learning_preferences enable row level security;

drop policy if exists "profiles_select_own" on public.profiles;
create policy "profiles_select_own"
on public.profiles for select
using (auth.uid() = user_id);

drop policy if exists "profiles_insert_own" on public.profiles;
create policy "profiles_insert_own"
on public.profiles for insert
with check (auth.uid() = user_id);

drop policy if exists "profiles_update_own" on public.profiles;
create policy "profiles_update_own"
on public.profiles for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

drop policy if exists "learning_preferences_select_own" on public.learning_preferences;
create policy "learning_preferences_select_own"
on public.learning_preferences for select
using (auth.uid() = user_id);

drop policy if exists "learning_preferences_insert_own" on public.learning_preferences;
create policy "learning_preferences_insert_own"
on public.learning_preferences for insert
with check (auth.uid() = user_id);

drop policy if exists "learning_preferences_update_own" on public.learning_preferences;
create policy "learning_preferences_update_own"
on public.learning_preferences for update
using (auth.uid() = user_id)
with check (auth.uid() = user_id);
