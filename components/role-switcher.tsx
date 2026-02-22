"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const TEACHER_PATH = "/teacher";
const STUDENT_PATH = "/onboarding";

export function RoleSwitcher() {
  const pathname = usePathname() ?? "";
  const isTeacher = pathname.startsWith(TEACHER_PATH);
  const href = isTeacher ? STUDENT_PATH : TEACHER_PATH;
  const label = isTeacher ? "Switch to Student" : "Switch to Teacher";
  const hint = isTeacher ? "Student view" : "Teacher view";

  return (
    <Link className="role-switch" href={href} aria-label={label}>
      <span className="role-switch-label">{label}</span>
      <span className="role-switch-meta">{hint}</span>
    </Link>
  );
}
