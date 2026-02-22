const summaryMetrics = [
  { label: "Active today", value: "86", detail: "+12 vs. last week", tone: "good" },
  { label: "Avg. mastery", value: "78%", detail: "+6% since unit 3", tone: "good" },
  { label: "Needs focus", value: "14", detail: "5 new this week", tone: "warn" },
  { label: "Stalled tasks", value: "8", detail: "2 overdue > 5 days", tone: "risk" }
];

const momentum = [
  { day: "Mon", value: 72 },
  { day: "Tue", value: 81 },
  { day: "Wed", value: 66 },
  { day: "Thu", value: 90 },
  { day: "Fri", value: 77 },
  { day: "Sat", value: 58 },
  { day: "Sun", value: 64 }
];

const focusStudents = [
  {
    name: "Ava Tran",
    unit: "Quadratic graphs",
    mastery: 92,
    status: "On track",
    statusClass: "good",
    note: "Accelerated pace, ready for enrichment"
  },
  {
    name: "Marcus Lee",
    unit: "Systems of equations",
    mastery: 61,
    status: "Watch",
    statusClass: "warn",
    note: "Hesitates on elimination steps"
  },
  {
    name: "Priya Desai",
    unit: "Polynomial factoring",
    mastery: 49,
    status: "At risk",
    statusClass: "risk",
    note: "Missed 2 sessions this week"
  },
  {
    name: "Noah Kim",
    unit: "Linear transformations",
    mastery: 70,
    status: "Watch",
    statusClass: "warn",
    note: "Needs more graphing practice"
  }
];

const classSnapshots = [
  {
    name: "Algebra II - Period 1",
    students: 28,
    mastery: 82,
    focus: "Function transformations",
    next: "Mini-lab: vertex shifts"
  },
  {
    name: "Geometry - Period 3",
    students: 31,
    mastery: 74,
    focus: "Similarity proofs",
    next: "Checkpoint: triangle similarity"
  },
  {
    name: "Pre-Calc - Period 5",
    students: 26,
    mastery: 79,
    focus: "Trigonometric identities",
    next: "Workshop: simplifying expressions"
  }
];

const interventions = [
  {
    title: "Small group: factoring basics",
    detail: "5 students flagged from last quiz",
    action: "Schedule 15-min clinic"
  },
  {
    title: "Review pack: system solving",
    detail: "Auto-assigned to 11 students",
    action: "Send encouragement note"
  },
  {
    title: "Pacing adjustment",
    detail: "2 students set to light pace",
    action: "Check in after lesson 4"
  }
];

const activityFeed = [
  {
    time: "9:14 AM",
    text: "Ava Tran completed “Quadratic forms” with 96% mastery."
  },
  {
    time: "8:52 AM",
    text: "Marcus Lee requested a hint on elimination step 3."
  },
  {
    time: "Yesterday",
    text: "Geometry Period 3 finished the similarity checkpoint."
  },
  {
    time: "Yesterday",
    text: "Priya Desai missed the review quiz; auto-reminder sent."
  }
];

export default function TeacherDashboardPage() {
  return (
    <div className="teacher-shell">
      <header className="teacher-hero">
        <div className="teacher-hero-copy">
          <p className="teacher-kicker">Teacher dashboard</p>
          <h1 className="teacher-title">Your Erica classroom at a glance</h1>
          <p className="teacher-subtitle">
            4 cohorts, 115 students, and a live pulse of where help is needed most.
          </p>
          <div className="teacher-chip-row">
            <span className="teacher-chip">Week 6 of 18</span>
            <span className="teacher-chip">Spring term</span>
            <span className="teacher-chip">Last sync 5 min ago</span>
          </div>
        </div>
        <div className="teacher-hero-card">
          <p className="teacher-card-kicker">Today&apos;s pulse</p>
          <h2 className="teacher-hero-metric">86 active learners</h2>
          <p className="teacher-hero-detail">Peak focus window: 9:00-10:30 AM</p>
          <div className="teacher-hero-grid">
            <div>
              <span className="teacher-hero-label">Assignments due</span>
              <strong className="teacher-hero-value">12</strong>
            </div>
            <div>
              <span className="teacher-hero-label">Auto-reminders</span>
              <strong className="teacher-hero-value">7 sent</strong>
            </div>
            <div>
              <span className="teacher-hero-label">New insights</span>
              <strong className="teacher-hero-value">3 flags</strong>
            </div>
          </div>
        </div>
      </header>

      <div className="teacher-main">
        <div className="teacher-left">
          <section className="teacher-card teacher-metrics">
            <div className="teacher-card-header">
              <h2>Class health</h2>
              <span className="teacher-meta">Updated in real time</span>
            </div>
            <div className="teacher-metric-grid">
              {summaryMetrics.map((metric) => (
                <div key={metric.label} className="teacher-metric-card">
                  <span className="teacher-metric-label">{metric.label}</span>
                  <strong className="teacher-metric-value">{metric.value}</strong>
                  <span className={`teacher-metric-detail ${metric.tone}`}>{metric.detail}</span>
                </div>
              ))}
            </div>
          </section>

          <section className="teacher-card teacher-chart">
            <div className="teacher-card-header">
              <h2>Weekly engagement</h2>
              <span className="teacher-meta">Average session length 24 min</span>
            </div>
            <div className="teacher-chart-body">
              <div className="teacher-chart-bars">
                {momentum.map((point) => (
                  <div key={point.day} className="teacher-chart-bar">
                    <span style={{ height: `${point.value}%` }} />
                  </div>
                ))}
              </div>
              <div className="teacher-chart-labels">
                {momentum.map((point) => (
                  <span key={point.day}>{point.day}</span>
                ))}
              </div>
            </div>
          </section>

          <section className="teacher-card teacher-roster">
            <div className="teacher-card-header">
              <h2>Students needing attention</h2>
              <span className="teacher-meta">Sorted by urgency</span>
            </div>
            <ul className="teacher-roster-list">
              {focusStudents.map((student) => (
                <li key={student.name} className="teacher-roster-row">
                  <div>
                    <div className="teacher-roster-name">{student.name}</div>
                    <div className="teacher-roster-meta">{student.unit}</div>
                    <div className="teacher-roster-note">{student.note}</div>
                  </div>
                  <div className="teacher-roster-progress">
                    <div className="teacher-progress-track">
                      <div
                        className="teacher-progress-fill"
                        style={{ width: `${student.mastery}%` }}
                      />
                    </div>
                    <div className="teacher-progress-meta">
                      <span className="teacher-progress-value">{student.mastery}% mastery</span>
                      <span className={`teacher-badge ${student.statusClass}`}>{student.status}</span>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </section>
        </div>

        <div className="teacher-right">
          <section className="teacher-card teacher-classes">
            <div className="teacher-card-header">
              <h2>Class snapshots</h2>
              <span className="teacher-meta">Next up: Pre-Calc workshop</span>
            </div>
            <div className="teacher-class-list">
              {classSnapshots.map((item) => (
                <div key={item.name} className="teacher-class-card">
                  <div className="teacher-class-header">
                    <h3>{item.name}</h3>
                    <span>{item.students} students</span>
                  </div>
                  <div className="teacher-class-meta">
                    <div>
                      <span className="teacher-class-label">Avg mastery</span>
                      <strong>{item.mastery}%</strong>
                    </div>
                    <div>
                      <span className="teacher-class-label">Focus</span>
                      <strong>{item.focus}</strong>
                    </div>
                  </div>
                  <p className="teacher-class-next">Next: {item.next}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="teacher-card teacher-interventions">
            <div className="teacher-card-header">
              <h2>Intervention queue</h2>
              <span className="teacher-meta">Suggested by Erica</span>
            </div>
            <ul className="teacher-intervention-list">
              {interventions.map((item) => (
                <li key={item.title}>
                  <h3>{item.title}</h3>
                  <p>{item.detail}</p>
                  <button className="teacher-action" type="button">
                    {item.action}
                  </button>
                </li>
              ))}
            </ul>
          </section>

          <section className="teacher-card teacher-activity">
            <div className="teacher-card-header">
              <h2>Recent activity</h2>
              <span className="teacher-meta">Last 24 hours</span>
            </div>
            <ul className="teacher-activity-list">
              {activityFeed.map((item, index) => (
                <li key={`${item.time}-${index}`}>
                  <span>{item.time}</span>
                  <p>{item.text}</p>
                </li>
              ))}
            </ul>
          </section>
        </div>
      </div>
    </div>
  );
}
