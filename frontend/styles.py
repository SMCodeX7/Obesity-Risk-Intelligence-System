import streamlit as st


APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Outfit:wght@500;600;700;800&display=swap');

/* ═══════════════════════════════════════
   DESIGN SYSTEM TOKENS
   - Edit these to retheme the entire app.
═══════════════════════════════════════ */
:root {
    /* ── Brand colors ── */
    --clr-primary:        #2563EB;
    --clr-primary-dark:   #1D4ED8;
    --clr-primary-deeper: #1E40AF;
    --clr-primary-light:  #EFF6FF;
    --clr-primary-muted:  rgba(37, 99, 235, 0.08);
    --clr-primary-border: #BFDBFE;
    --clr-primary-ring:   rgba(59, 130, 246, 0.16);

    /* ── Teal / success ── */
    --clr-teal:           #0D9488;
    --clr-teal-dark:      #0F766E;
    --clr-teal-light:     #F0FDFA;
    --clr-teal-border:    #99F6E4;
    --clr-teal-muted:     rgba(13, 148, 136, 0.08);

    /* ── Success green ── */
    --clr-success:        #16A34A;
    --clr-success-light:  #F0FDF4;
    --clr-success-border: #BBF7D0;

    /* ── Warning amber ── */
    --clr-warning:        #D97706;
    --clr-warning-light:  #FEFCE8;
    --clr-warning-border: #FEF08A;

    /* ── Risk red ── */
    --clr-danger:         #E11D48;
    --clr-danger-light:   #FFF1F2;
    --clr-danger-border:  #FECDD3;

    /* ── Neutral slate ── */
    --clr-ink:            #0F172A;
    --clr-ink-muted:      #1E293B;
    --clr-body:           #334155;
    --clr-subtle:         #475569;
    --clr-muted:          #64748B;
    --clr-placeholder:    #94A3B8;
    --clr-border:         #E2E8F0;
    --clr-border-soft:    rgba(226, 232, 240, 0.7);
    --clr-surface:        #FFFFFF;
    --clr-surface-2:      #F8FAFC;
    --clr-surface-3:      #F1F5F9;
    --clr-app-bg:         #F8FAFC;

    /* ── Border radius scale ── */
    --radius-xs:  8px;
    --radius-sm:  12px;
    --radius-md:  16px;
    --radius-lg:  20px;
    --radius-xl:  24px;
    --radius-2xl: 28px;
    --radius-pill: 999px;

    /* ── Shadow scale ── */
    --shadow-xs:  0 1px 3px rgba(15, 23, 42, 0.04);
    --shadow-sm:  0 2px 8px -2px rgba(15, 23, 42, 0.05), inset 0 1px 0 rgba(255,255,255,0.9);
    --shadow-md:  0 4px 16px -4px rgba(15, 23, 42, 0.06), inset 0 1px 0 rgba(255,255,255,0.95);
    --shadow-lg:  0 10px 28px -6px rgba(15, 23, 42, 0.07), inset 0 1px 0 rgba(255,255,255,0.95);
    --shadow-xl:  0 16px 40px -8px rgba(15, 23, 42, 0.08), inset 0 1px 0 rgba(255,255,255,0.95);
    --shadow-blue-sm: 0 4px 14px rgba(37, 99, 235, 0.22);
    --shadow-blue-md: 0 8px 24px rgba(37, 99, 235, 0.30);

    /* ── Spacing scale ── */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.25rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-10: 2.5rem;

    /* ── Transitions ── */
    --ease-spring: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-out: cubic-bezier(0.4, 0, 0.2, 1);
    --transition-fast: 0.18s;
    --transition-base: 0.22s;
    --transition-slow: 0.3s;
}

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, .health-hero-title, .health-page-title, .health-stat-value {
    font-family: 'Outfit', 'Plus Jakarta Sans', -apple-system, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 92% 3%,
            rgba(59, 130, 246, 0.08),
            transparent 32rem
        ),
        radial-gradient(
            circle at 6% 20%,
            rgba(20, 184, 166, 0.05),
            transparent 28rem
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(241, 245, 249, 0.8),
            transparent 40rem
        ),
        #F8FAFC;
}


.block-container {
    max-width: 1240px;
    padding-top: 2rem;
    padding-bottom: 3.5rem;
}


.health-hero {
    position: relative;
    overflow: hidden;

    padding: 3.2rem 3.4rem;

    border: 1px solid rgba(219, 234, 254, 0.95);
    border-radius: 28px;

    background:
        radial-gradient(
            circle at 95% 12%,
            rgba(37, 99, 235, 0.08) 0%,
            transparent 22rem
        ),
        radial-gradient(
            circle at 4% 92%,
            rgba(13, 148, 136, 0.06) 0%,
            transparent 24rem
        ),
        radial-gradient(
            circle at 50% 0%,
            rgba(239, 246, 255, 0.6) 0%,
            transparent 32rem
        ),
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #F8FBFF 48%,
            #EFF6FF 100%
        );

    box-shadow:
        0 20px 45px -15px rgba(15, 23, 42, 0.06),
        0 1px 3px 0 rgba(15, 23, 42, 0.02),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.95);
}


.health-hero::after {
    content: "";

    position: absolute;

    width: 320px;
    height: 320px;

    right: -80px;
    bottom: -110px;

    border-radius: 50%;

    border: 1px dashed rgba(37, 99, 235, 0.16);
    background: radial-gradient(circle, rgba(59, 130, 246, 0.035) 0%, transparent 70%);
    pointer-events: none;
}


.health-hero::before {
    content: "";

    position: absolute;

    width: 180px;
    height: 180px;

    right: 70px;
    bottom: 40px;

    border-radius: 50%;

    border: 1px solid rgba(13, 148, 136, 0.12);
    pointer-events: none;
}


.health-eyebrow {
    display: inline-flex;

    align-items: center;

    gap: 0.65rem;

    padding:
        0.45rem
        0.95rem;

    margin-bottom: 1.35rem;

    border-radius: 999px;

    border:
        1px solid rgba(191, 219, 254, 0.85);

    background:
        rgba(
            255,
            255,
            255,
            0.94
        );

    backdrop-filter: blur(10px);

    box-shadow:
        0 2px 8px rgba(37, 99, 235, 0.06);

    color: #1D4ED8;

    font-size: 0.74rem;
    font-weight: 750;

    letter-spacing: 0.08em;
    text-transform: uppercase;
}


.health-eyebrow-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #10B981;

    box-shadow:
        0 0 0 4px
        rgba(16, 185, 129, 0.2);

    animation: health-pulse 2.2s infinite cubic-bezier(0.4, 0, 0.6, 1);
}


@keyframes health-pulse {
    0%, 100% {
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.25);
    }
    50% {
        box-shadow: 0 0 0 7px rgba(16, 185, 129, 0.06);
    }
}


.health-eyebrow-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.09);
    color: #2563EB;
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}


.health-hero-title {
    max-width: 880px;

    margin: 0;

    color: #0F172A;

    font-size:
        clamp(
            2.4rem,
            4.6vw,
            3.8rem
        );

    line-height: 1.08;

    letter-spacing: -0.04em;

    font-weight: 800;
}


.health-hero-title span,
.health-hero-gradient {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 42%, #0284C7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.health-hero-description {
    max-width: 860px;

    margin:
        1.35rem
        0
        0;

    color: #475569;

    font-size: 1.05rem;

    line-height: 1.78;
    letter-spacing: -0.01em;
}


.health-stats {
    display: grid;

    grid-template-columns:
        repeat(
            3,
            minmax(0, 1fr)
        );

    gap: 1.35rem;

    width: 100%;
    max-width: 100%;

    margin-top: 2.4rem;
}


.health-stat {
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    min-height: 154px;

    padding:
        1.45rem
        1.65rem;

    border: 1px solid
        rgba(
            226,
            232,
            240,
            0.9
        );

    border-radius: 20px;

    background:
        rgba(
            255,
            255,
            255,
            0.85
        );

    backdrop-filter:
        blur(14px);

    box-shadow:
        0 4px 16px -2px rgba(15, 23, 42, 0.04),
        0 1px 2px 0 rgba(15, 23, 42, 0.02),
        inset 0 1px 0 0 rgba(255, 255, 255, 0.95);

    transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}


.health-stat::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: transparent;
    transition: background 0.3s ease;
}


.health-stat:hover {
    transform: translateY(-4px);
    background: rgba(255, 255, 255, 0.98);
    border-color: rgba(147, 197, 253, 0.85);
    box-shadow:
        0 16px 36px -8px rgba(37, 99, 235, 0.12),
        0 4px 12px 0 rgba(15, 23, 42, 0.04),
        inset 0 1px 0 0 rgba(255, 255, 255, 1);
}


.health-stat:hover::before {
    background: linear-gradient(90deg, #2563EB, #0284C7);
}


.health-stat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.9rem;
}


.health-stat-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.22rem 0.62rem;
    border-radius: 999px;
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}


.tag-accent-blue {
    background: rgba(37, 99, 235, 0.08);
    color: #1D4ED8;
    border: 1px solid rgba(191, 219, 254, 0.7);
}


.tag-accent-teal {
    background: rgba(13, 148, 136, 0.08);
    color: #0F766E;
    border: 1px solid rgba(153, 246, 228, 0.7);
}


.tag-accent-indigo {
    background: rgba(79, 70, 229, 0.08);
    color: #4338CA;
    border: 1px solid rgba(199, 210, 254, 0.7);
}


.health-stat-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 10px;
    transition: transform 0.25s ease;
}


.health-stat:hover .health-stat-icon {
    transform: scale(1.08);
}


.icon-blue {
    background: rgba(239, 246, 255, 0.95);
    color: #2563EB;
}


.icon-teal {
    background: rgba(240, 253, 250, 0.95);
    color: #0D9488;
}


.icon-indigo {
    background: rgba(238, 242, 255, 0.95);
    color: #4F46E5;
}

.icon-target {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%232563EB' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Ccircle cx='12' cy='12' r='6'/%3E%3Ccircle cx='12' cy='12' r='2'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
}

.icon-pulse {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%230D9488' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='22 12 18 12 15 21 9 3 6 12 2 12'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
}

.icon-shield {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%234F46E5' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: center;
}


.health-stat-body {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}


.health-stat-value {
    display: block;

    color: #0F172A;

    font-size: 2.15rem;

    font-weight: 800;

    line-height: 1.1;

    letter-spacing: -0.035em;
}


.health-stat-label {
    display: block;

    margin-top: 0.2rem;

    color: #475569;

    font-size: 0.74rem;

    font-weight: 700;

    letter-spacing: 0.06em;

    text-transform: uppercase;
}


.health-stat-footer {
    margin-top: 0.85rem;
    padding-top: 0.7rem;
    border-top: 1px solid rgba(226, 232, 240, 0.65);
}


.health-stat-desc {
    display: block;
    color: #64748B;
    font-size: 0.72rem;
    font-weight: 500;
    line-height: 1.4;
}


/* Navigation Pills Modernization */
div[data-testid="stPills"] {
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 999px;
    padding: 0.32rem 0.45rem;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    backdrop-filter: blur(10px);
}

div[data-testid="stPills"] button {
    border-radius: 999px !important;
    font-weight: 650 !important;
    font-size: 0.86rem !important;
    transition: all 0.2s ease !important;
}

/* Sidebar Polish */
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 1.32rem !important;
    white-space: nowrap !important;
    text-overflow: clip !important;
    overflow: visible !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 650 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}


.health-page-header {
    margin:
        2.2rem
        0
        1.25rem;
}


.health-page-kicker {
    margin-bottom: 0.35rem;

    color: #2563EB;

    font-size: 0.75rem;

    font-weight: 760;

    letter-spacing: 0.085em;

    text-transform: uppercase;
}


.health-page-title {
    margin: 0;

    color: #0F172A;

    font-size: 1.8rem;

    line-height: 1.2;

    letter-spacing: -0.035em;

    font-weight: 760;
}


.health-page-description {
    max-width: 700px;

    margin-top: 0.55rem;

    color: #64748B;

    font-size: 0.95rem;

    line-height: 1.7;
}


/* ==========================================================================
   HEALTHCARE DASHBOARD - ASSESSMENT FORM & STEPPER STYLES
   ========================================================================== */

.health-stepper-container {
    margin: 1.35rem 0 1.6rem;
}

/* Progress Indicator Panel (Step X of 3 / Title / ━━━━━━○○○ style) */
.health-progress-panel {
    padding: 1.4rem 1.65rem;
    margin-bottom: 1.25rem;
    border: 1px solid rgba(219, 234, 254, 0.95);
    border-radius: 22px;
    background:
        radial-gradient(circle at 95% 10%, rgba(37, 99, 235, 0.06) 0%, transparent 40%),
        linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 50%, #EFF6FF 100%);
    box-shadow:
        0 4px 20px -4px rgba(15, 23, 42, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);
}

.health-progress-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.15rem;
}

.health-progress-meta {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

.health-progress-step-pill {
    display: inline-flex;
    align-items: center;
    width: fit-content;
    padding: 0.22rem 0.72rem;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.1);
    color: #2563EB;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.health-progress-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 1.38rem;
    font-weight: 750;
    color: #0F172A;
    margin: 0;
    letter-spacing: -0.025em;
    line-height: 1.2;
}

.health-progress-pct-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    background: #EFF6FF;
    border: 1px solid rgba(147, 197, 253, 0.6);
    color: #1D4ED8;
    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.02em;
}

/* Visual Bar + Nodes: ━━━━━━○○○ style */
.health-progress-visual {
    margin-top: 0.35rem;
}

.health-progress-bar-track {
    position: relative;
    width: 100%;
    height: 7px;
    background: #E2E8F0;
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 0.95rem;
}

.health-progress-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563EB 0%, #0D9488 100%);
    transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.health-progress-bar-fill.step-1 {
    width: 33.33%;
}

.health-progress-bar-fill.step-2 {
    width: 66.66%;
}

.health-progress-bar-fill.step-3 {
    width: 100%;
}

.health-progress-dots-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
}

.health-dot-node {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.76rem;
    font-weight: 600;
    color: #94A3B8;
    transition: all 0.2s ease;
}

.health-dot-node.active {
    color: #2563EB;
    font-weight: 750;
}

.health-dot-node.complete {
    color: #0D9488;
    font-weight: 700;
}

.health-dot-circle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 800;
    line-height: 1;
    background: #F1F5F9;
    border: 1.5px solid #CBD5E1;
    color: #94A3B8;
    transition: all 0.2s ease;
}

.health-dot-node.active .health-dot-circle {
    background: #2563EB;
    border-color: #2563EB;
    color: #FFFFFF;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.18);
}

.health-dot-node.complete .health-dot-circle {
    background: #0D9488;
    border-color: #0D9488;
    color: #FFFFFF;
}

/* Stepper Cards Grid */
.health-stepper-cards {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}

.health-step-card {
    display: flex;
    flex-direction: column;
    padding: 1rem 1.15rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-lg);
    background: var(--clr-surface);
    transition: all var(--transition-base) var(--ease-spring);
}

.health-step-card.active {
    border-color: #93C5FD;
    background:
        radial-gradient(circle at 90% 10%, rgba(37, 99, 235, 0.05) 0%, transparent 50%),
        linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
    box-shadow:
        0 6px 20px -4px rgba(37, 99, 235, 0.12),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.health-step-card.complete {
    border-color: #99F6E4;
    background:
        radial-gradient(circle at 90% 10%, rgba(13, 148, 136, 0.05) 0%, transparent 50%),
        linear-gradient(135deg, #F0FDFA 0%, #FFFFFF 100%);
}

.health-step-card.upcoming {
    opacity: 0.72;
    background: #FAFAFC;
}

.health-step-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.65rem;
}

.health-step-number-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.76rem;
    font-weight: 800;
    background: #F1F5F9;
    color: #64748B;
}

.health-step-card.active .health-step-number-circle {
    background: #2563EB;
    color: #FFFFFF;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.health-step-card.complete .health-step-number-circle {
    background: #CCFBF1;
    color: #0F766E;
}

.health-step-badge {
    font-size: 0.64rem;
    font-weight: 750;
    padding: 0.16rem 0.58rem;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.health-step-badge.current {
    background: #DBEAFE;
    color: #1D4ED8;
    border: 1px solid rgba(29, 78, 216, 0.15);
}

.health-step-badge.done {
    background: #CCFBF1;
    color: #0F766E;
    border: 1px solid rgba(15, 118, 110, 0.15);
}

.health-step-badge.pending {
    background: #F1F5F9;
    color: #94A3B8;
    border: 1px solid #E2E8F0;
}

.health-step-card-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 0.92rem;
    font-weight: 750;
    color: #0F172A;
    margin-bottom: 0.2rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.health-step-card.active .health-step-card-title {
    color: #1D4ED8;
}

.health-step-card.complete .health-step-card-title {
    color: #0F766E;
}

.health-step-card-desc {
    font-size: 0.74rem;
    color: #64748B;
    line-height: 1.45;
}

/* Legacy Stepper Compatibility */
.health-stepper {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.7rem;
    margin: 1.3rem 0 1.4rem;
}

.health-step {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.82rem 0.95rem;
    border: 1px solid #E2E8F0;
    border-radius: 17px;
    background: #FFFFFF;
    transition: border-color 0.2s ease, background 0.2s ease;
}

.health-step.active {
    border-color: #93C5FD;
    background: #EFF6FF;
}

.health-step.complete {
    border-color: #CCFBF1;
    background: #F0FDFA;
}

.health-step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 31px;
    height: 31px;
    flex: 0 0 31px;
    border-radius: 50%;
    background: #F1F5F9;
    color: #64748B;
    font-size: 0.78rem;
    font-weight: 750;
}

.health-step.active .health-step-number {
    background: #2563EB;
    color: #FFFFFF;
}

.health-step.complete .health-step-number {
    background: #CCFBF1;
    color: #0F766E;
}

.health-step-name {
    color: #475569;
    font-size: 0.83rem;
    font-weight: 650;
}

.health-step.active .health-step-name {
    color: #1D4ED8;
}

.health-step.complete .health-step-name {
    color: #0F766E;
}

/* Step Information Card */
.health-info-card {
    display: flex;
    align-items: flex-start;
    gap: 1.1rem;
    padding: 1.15rem 1.4rem;
    margin-bottom: 1.35rem;
    border: 1px solid rgba(219, 234, 254, 0.9);
    border-radius: var(--radius-lg);
    background:
        radial-gradient(circle at 95% 15%, rgba(37, 99, 235, 0.05) 0%, transparent 45%),
        linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
    box-shadow: var(--shadow-sm);
}

.health-info-icon {
    flex-shrink: 0;
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid rgba(147, 197, 253, 0.6);
    color: #2563EB;
    font-size: 0.88rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08);
}

.health-info-content {
    flex: 1 1 auto;
}

.health-info-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 750;
    color: #0F172A;
    letter-spacing: -0.01em;
}

.health-info-text {
    margin-top: 0.22rem;
    color: #64748B;
    font-size: 0.84rem;
    line-height: 1.6;
}

/* ── Form Container & Section Cards ── */
[data-testid="stForm"] {
    border: 1px solid rgba(219, 234, 254, 0.95) !important;
    border-radius: 24px !important;
    background:
        radial-gradient(circle at 98% 3%, rgba(37, 99, 235, 0.04) 0%, transparent 35%),
        linear-gradient(135deg, #FFFFFF 0%, #FAFCFF 100%) !important;
    box-shadow:
        0 8px 30px -8px rgba(15, 23, 42, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
    padding: 1.8rem 2rem !important;
}

[data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid rgba(226, 232, 240, 0.9) !important;
    border-radius: 20px !important;
    background:
        linear-gradient(135deg, #FFFFFF 0%, #F9FBFC 100%) !important;
    box-shadow:
        0 2px 10px rgba(15, 23, 42, 0.03),
        inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
    padding: 1.45rem 1.6rem !important;
    margin-bottom: 1.25rem !important;
    transition: border-color 0.22s ease, box-shadow 0.22s ease !important;
}

[data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(147, 197, 253, 0.75) !important;
    box-shadow:
        0 6px 18px -4px rgba(37, 99, 235, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.95) !important;
}

/* Section Header Component */
.health-section-header {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid rgba(226, 232, 240, 0.7);
}

.health-section-icon-wrap {
    flex-shrink: 0;
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid rgba(147, 197, 253, 0.6);
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08);
}

.health-section-text-wrap {
    flex: 1 1 auto;
}

.health-section-kicker {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.075em;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 0.12rem;
}

.health-section-header .health-section-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 750;
    color: #0F172A;
    letter-spacing: -0.02em;
    margin: 0;
    padding: 0;
    background: none;
}

.health-section-subtitle {
    font-size: 0.81rem;
    color: #64748B;
    margin-top: 0.15rem;
    line-height: 1.45;
}

/* ── Modern Form Input Polish ── */
[data-testid="stWidgetLabel"] label,
[data-testid="stWidgetLabel"] p {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 650 !important;
    color: #1E293B !important;
    letter-spacing: -0.01em !important;
    margin-bottom: 0.35rem !important;
}

[data-testid="stNumberInput"] input {
    border-radius: 12px !important;
    border: 1.5px solid #CBD5E1 !important;
    background: #FFFFFF !important;
    font-size: 0.94rem !important;
    font-weight: 600 !important;
    color: #0F172A !important;
    height: 42px !important;
    padding: 0.5rem 0.85rem !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16) !important;
}

[data-testid="stNumberInput"] button {
    border-radius: 8px !important;
    transition: background 0.15s ease !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    border-radius: 12px !important;
    border: 1.5px solid #CBD5E1 !important;
    background: #FFFFFF !important;
    min-height: 42px !important;
    font-size: 0.92rem !important;
    font-weight: 550 !important;
    color: #0F172A !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.16) !important;
}

[data-testid="stSlider"] {
    padding-top: 0.35rem !important;
    padding-bottom: 0.55rem !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 750 !important;
    color: #2563EB !important;
    font-size: 0.92rem !important;
}

/* Form Submit Buttons */
[data-testid="stFormSubmitButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 60%, #3B82F6 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.84rem 1.65rem !important;
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    color: #FFFFFF !important;
    box-shadow:
        0 4px 14px rgba(37, 99, 235, 0.32),
        inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%) !important;
    box-shadow:
        0 8px 22px rgba(37, 99, 235, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stFormSubmitButton"] > button[kind="primary"]:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.28) !important;
}

[data-testid="stFormSubmitButton"] > button[kind="secondary"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 14px !important;
    padding: 0.84rem 1.65rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 650 !important;
    color: #475569 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFormSubmitButton"] > button[kind="secondary"]:hover {
    background: #F8FAFC !important;
    border-color: #94A3B8 !important;
    color: #0F172A !important;
    transform: translateY(-1px) !important;
}

/* Context Hint Helper */
.health-field-hint {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 68px;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    background: rgba(241, 245, 249, 0.75);
    border: 1px dashed #CBD5E1;
    margin-top: 1.6rem;
}

.health-hint-badge {
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    color: #2563EB;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
}

.health-hint-desc {
    font-size: 0.78rem;
    color: #475569;
    line-height: 1.45;
}



.health-card {
    padding: 1.4rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-xl);
    background: var(--clr-surface);
    box-shadow: var(--shadow-md);
    transition: transform var(--transition-base) var(--ease-spring),
                box-shadow var(--transition-base) var(--ease-out);
}

.health-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.health-result-card {
    padding: 1.5rem;
    border: 1px solid var(--clr-primary-border);
    border-radius: var(--radius-xl);
    background: linear-gradient(135deg, #FFFFFF, #F8FBFF);
    box-shadow: var(--shadow-md);
}


.health-result-label {
    color: #64748B;

    font-size: 0.74rem;

    font-weight: 700;

    letter-spacing: 0.075em;

    text-transform: uppercase;
}


.health-result-title {
    margin-top: 0.35rem;

    color: #0F172A;

    font-size: 2rem;

    font-weight: 780;

    letter-spacing: -0.04em;
}


.health-notice {
    display: flex;
    align-items: flex-start;
    gap: 0.95rem;
    padding: 1.15rem 1.35rem;
    border: 1px solid rgba(20, 184, 166, 0.28);
    border-radius: var(--radius-lg);
    background:
        radial-gradient(circle at 95% 15%, rgba(13, 148, 136, 0.05) 0%, transparent 45%),
        linear-gradient(135deg, #F0FDFA 0%, #ECFEFF 100%);
    margin-top: 1rem;
    margin-bottom: 0.8rem;
    color: #134E4A;
    font-size: 0.84rem;
    line-height: 1.55;
}

.health-notice-icon {
    flex-shrink: 0;
    font-size: 1.3rem;
    line-height: 1;
    margin-top: 0.1rem;
}

.health-notice-body strong {
    display: block;
    font-family: 'Outfit', sans-serif;
    color: #0F766E;
    font-size: 0.92rem;
    font-weight: 750;
    margin-bottom: 0.25rem;
}

.health-notice-body p {
    color: #134E4A;
    font-size: 0.83rem;
    line-height: 1.55;
    margin: 0;
}

.health-notice.ready-notice {
    border-color: rgba(99, 102, 241, 0.25);
    background:
        radial-gradient(circle at 95% 15%, rgba(99, 102, 241, 0.06) 0%, transparent 45%),
        linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 100%);
}

.health-notice.ready-notice .health-notice-body strong {
    color: #4338CA;
}

.health-notice.ready-notice .health-notice-body p {
    color: #3730A3;
}



.health-sidebar-brand {
    padding:
        0.8rem
        0
        1rem;
}


.health-sidebar-row {
    display: flex;

    align-items: center;

    gap: 0.75rem;
}


.health-sidebar-logo {
    display: flex;

    align-items: center;
    justify-content: center;

    width: 44px;
    height: 44px;

    flex:
        0
        0
        44px;

    border-radius: 14px;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #0F8B8D
        );

    color: #FFFFFF;

    font-size: 0.8rem;

    font-weight: 800;

    letter-spacing: -0.02em;

    box-shadow:
        0 9px 24px
        rgba(
            37,
            99,
            235,
            0.17
        );
}


.health-sidebar-title {
    color: #0F172A;

    font-size: 0.91rem;

    font-weight: 760;

    line-height: 1.25;
}


.health-sidebar-subtitle {
    margin-top: 0.14rem;

    color: #94A3B8;

    font-size: 0.71rem;
}


.health-status {
    display: inline-flex;

    align-items: center;

    gap: 0.45rem;

    color: #475569;

    font-size: 0.8rem;
}


.health-status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #10B981;

    box-shadow:
        0 0 0 4px
        rgba(
            16,
            185,
            129,
            0.10
        );
}


.health-footer {
    padding-top: 1.4rem;

    margin-top: 2.5rem;

    border-top:
        1px solid #E2E8F0;

    color: #94A3B8;

    font-size: 0.77rem;

    line-height: 1.65;
}


.health-result-summary {
    padding: 2.2rem 2.4rem;
    border: 1px solid var(--clr-primary-border);
    border-radius: var(--radius-2xl);
    background:
        radial-gradient(circle at 95% 8%, rgba(37, 99, 235, 0.05) 0%, transparent 45%),
        linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 55%, #EFF6FF 100%);
    box-shadow: var(--shadow-lg);
    transition: box-shadow var(--transition-slow) ease;
}

.health-result-summary:hover {
    box-shadow: var(--shadow-xl);
}

.health-result-top {
    display: grid;
    grid-template-columns: 1fr 240px;
    gap: 2rem;
    align-items: stretch;
}

.health-result-main-col {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.health-result-eyebrow-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 0.65rem;
}

.health-result-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.28rem 0.75rem;
    border-radius: 999px;
    background: rgba(37, 99, 235, 0.08);
    color: #1D4ED8;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
}

.health-result-live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

.health-result-risk-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.28rem 0.8rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 750;
    letter-spacing: 0.02em;
}

.health-result-category {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 2.85rem;
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -0.035em;
    margin: 0.35rem 0 0.85rem 0;
}

.health-result-description-card {
    display: flex;
    align-items: flex-start;
    gap: 0.85rem;
    padding: 0.95rem 1.2rem;
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(226, 232, 240, 0.9);
    backdrop-filter: blur(8px);
    max-width: 680px;
}

.health-result-desc-icon {
    font-size: 1.15rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}

.health-result-desc-text {
    font-size: 0.86rem;
    color: #475569;
    line-height: 1.55;
    margin: 0;
}

/* ── Visual Confidence Card (Dial + Progress Meter) ── */
.health-confidence-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    min-width: 220px;
    padding: 1.3rem 1.35rem;
    border-radius: var(--radius-xl);
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(12px);
    border: 1px solid var(--clr-primary-border);
    box-shadow: var(--shadow-md);
    transition: transform var(--transition-base) var(--ease-spring), box-shadow var(--transition-base) ease;
}

.health-confidence-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg);
}

.health-confidence-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 0.5rem;
}

.health-confidence-kicker {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #64748B;
}

.health-confidence-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.15rem 0.55rem;
    border-radius: 999px;
    font-size: 0.65rem;
    font-weight: 750;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* Circular Conic Dial Gauge */
.health-confidence-dial-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0.75rem 0;
}

.health-confidence-dial {
    width: 104px;
    height: 104px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    transition: transform 0.3s ease;
}

.health-confidence-dial-inner {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
}

.health-confidence-number {
    font-family: 'Outfit', sans-serif;
    font-size: 1.42rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
}

.health-confidence-pct-sign {
    font-size: 0.82rem;
    font-weight: 700;
    margin-left: 1px;
}

.health-confidence-caption {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    color: #64748B;
    letter-spacing: 0.06em;
    margin-top: 0.18rem;
}

/* Linear Progress Meter Bar */
.health-confidence-meter-container {
    width: 100%;
}

.health-confidence-bar-track {
    width: 100%;
    height: 6px;
    background: #E2E8F0;
    border-radius: 999px;
    overflow: hidden;
    margin-bottom: 0.35rem;
}

.health-confidence-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

.health-confidence-scale-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.64rem;
    font-weight: 600;
    color: #94A3B8;
}

/* Fallback box */
.health-confidence-box {
    display: none;
}

/* ── Metadata Cards ── */
.health-result-meta {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.95rem;
    margin-top: 1.5rem;
    padding-top: 1.35rem;
    border-top: 1px solid rgba(226, 232, 240, 0.75);
}

.health-result-meta-item {
    display: flex;
    align-items: center;
    gap: 0.95rem;
    padding: 0.95rem 1.2rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-lg);
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow-xs);
    transition:
        transform var(--transition-base) var(--ease-spring),
        box-shadow var(--transition-base) ease,
        border-color var(--transition-base) ease;
}

.health-result-meta-item:hover {
    transform: translateY(-3px);
    border-color: rgba(147, 197, 253, 0.85);
    box-shadow:
        0 10px 24px -4px rgba(37, 99, 235, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);
}

.health-meta-icon-box {
    width: 42px;
    height: 42px;
    flex-shrink: 0;
    border-radius: 12px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid rgba(147, 197, 253, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.08);
}

.health-meta-content {
    flex: 1 1 auto;
    min-width: 0;
}

.health-result-meta-label {
    color: #64748B;
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.health-result-meta-value {
    margin-top: 0.12rem;
    color: #0F172A;
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 0.98rem;
    font-weight: 750;
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.health-meta-sub {
    color: #94A3B8;
    font-size: 0.7rem;
    margin-top: 0.08rem;
}



.health-probability-section {
    margin-top: 1.4rem;
}


.health-section-title {
    margin-top: 1rem;
    margin-bottom: 0.8rem;
    padding: 0.7rem 1rem;
    border-radius: var(--radius-sm);
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.08), rgba(15, 139, 141, 0.08));
    color: #1E3A8A;
    font-size: 1rem;
    font-weight: 750;
}


.health-section-description {
    margin-top: 0.25rem;

    color: #64748B;

    font-size: 0.82rem;

    line-height: 1.55;
}


.health-probability-list {
    display: flex;

    flex-direction: column;

    gap: 0.8rem;

    margin-top: 1rem;
}


.health-probability-row {
    padding: 0.8rem 0.9rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, #FFFFFF, #FAFCFF);
    transition: transform var(--transition-base) var(--ease-spring),
                box-shadow var(--transition-base) ease;
}


.health-probability-row:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}


.health-probability-header {
    display: flex;

    justify-content: space-between;
    align-items: center;

    gap: 1rem;

    margin-bottom: 0.5rem;
}


.health-probability-name {
    color: #334155;

    font-size: 0.82rem;

    font-weight: 650;
}


.health-probability-value {
    color: #2563EB;

    font-size: 0.8rem;

    font-weight: 740;
}


.health-probability-track {
    width: 100%;
    height: 8px;

    overflow: hidden;

    border-radius: 999px;

    background: #E2E8F0;
}


.health-probability-fill {
    height: 100%;
    border-radius: var(--radius-pill);
    /* Color overridden inline per category; this fallback aligns with primary */
    background: var(--clr-primary);
}


.health-history-summary {
    display: grid;

    grid-template-columns:
        repeat(
            3,
            minmax(0, 1fr)
        );

    gap: 0.8rem;

    margin-bottom: 1.3rem;
}


.health-history-stat {
    padding: 1rem 1.1rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-lg);
    background: var(--clr-surface);
    box-shadow: var(--shadow-xs);
    transition: transform var(--transition-fast) var(--ease-spring),
                box-shadow var(--transition-fast) ease;
}

.health-history-stat:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
}


.health-history-stat-value {
    color: #0F172A;

    font-size: 1.35rem;

    font-weight: 760;
}


.health-history-stat-label {
    margin-top: 0.15rem;

    color: #64748B;

    font-size: 0.74rem;

    font-weight: 650;
}


.health-history-list {
    display: flex;

    flex-direction: column;

    gap: 0.85rem;

    margin-top: 1rem;
}


.health-history-card {
    padding: 1rem 1.1rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-lg);
    background: var(--clr-surface);
    box-shadow: var(--shadow-xs);
    transition:
        transform var(--transition-fast) var(--ease-spring),
        border-color var(--transition-fast) ease,
        box-shadow var(--transition-fast) ease;
}


.health-history-card:hover {
    transform: translateY(-1px);

    border-color: #BFDBFE;

    box-shadow:
        0 10px 24px
        rgba(
            15,
            23,
            42,
            0.045
        );
}


.health-history-header {
    display: flex;

    justify-content: space-between;
    align-items: center;

    gap: 1rem;

    flex-wrap: wrap;
}


.health-history-id {
    color: #2563EB;

    font-size: 0.75rem;

    font-weight: 740;
}


.health-history-date {
    color: #94A3B8;

    font-size: 0.75rem;
}


.health-history-category {
    margin-top: 0.45rem;

    color: #0F172A;

    font-size: 1.05rem;

    font-weight: 720;
}


.health-history-details {
    display: flex;

    gap: 1rem;

    flex-wrap: wrap;

    margin-top: 0.45rem;

    color: #64748B;

    font-size: 0.78rem;
}


.health-empty-state {
    padding: 2rem 1.5rem;

    text-align: center;

    border: 1px dashed #CBD5E1;

    border-radius: 22px;

    background: #FFFFFF;
}


.health-empty-icon {
    display: flex;

    align-items: center;
    justify-content: center;

    width: 48px;
    height: 48px;

    margin:
        0 auto
        0.9rem;

    border-radius: 15px;

    background: #EFF6FF;

    color: #2563EB;

    font-size: 1rem;

    font-weight: 780;
}


.health-empty-title {
    color: #0F172A;

    font-size: 1rem;

    font-weight: 720;
}


.health-empty-text {
    max-width: 460px;

    margin:
        0.4rem
        auto
        0;

    color: #64748B;

    font-size: 0.82rem;

    line-height: 1.6;
}


.health-detail-grid {
    display: grid;

    grid-template-columns:
        repeat(
            2,
            minmax(0, 1fr)
        );

    gap: 0.8rem;

    margin-top: 1rem;
}


.health-detail-card {
    padding: 1rem;

    border: 1px solid #E2E8F0;

    border-radius: 17px;

    background: #FFFFFF;
}


.health-detail-title {
    color: #2563EB;

    font-size: 0.72rem;

    font-weight: 740;

    letter-spacing: 0.065em;

    text-transform: uppercase;
}


.health-detail-value {
    margin-top: 0.25rem;

    color: #334155;

    font-size: 0.86rem;

    font-weight: 620;
}


.health-risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.02em;
    transition: transform 0.2s ease;
}

.health-risk-badge.insufficient {
    background: #E0F2FE;
    color: #0369A1;
    border: 1px solid rgba(3, 105, 161, 0.2);
}

.health-risk-badge.low {
    background: #DCFCE7;
    color: #166534;
    border: 1px solid rgba(22, 101, 52, 0.2);
}

.health-risk-badge.moderate {
    background: #FEF9C3;
    color: #854D0E;
    border: 1px solid rgba(133, 77, 14, 0.2);
}

.health-risk-badge.moderate-high {
    background: #FFEDD5;
    color: #9A3412;
    border: 1px solid rgba(154, 52, 18, 0.2);
}

.health-risk-badge.high {
    background: #FFE4E6;
    color: #BE123C;
    border: 1px solid rgba(190, 18, 60, 0.2);
}

.health-risk-badge.very-high {
    background: #FEE2E2;
    color: #B91C1C;
    border: 1px solid rgba(185, 28, 28, 0.2);
}

.health-risk-badge.severe {
    background: #FECACA;
    color: #7F1D1D;
    border: 1px solid rgba(127, 29, 29, 0.25);
}

.health-risk-badge.unknown {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #E2E8F0;
}


.health-explanation-card {

    margin-top: 1.5rem;

    padding: 1.25rem;

    border-radius: 18px;

    border: 1px solid #DBEAFE;

    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.05),
            rgba(15,139,141,0.05)
        );

}


.health-explanation-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 1rem;

    margin-top: 1rem;

}


.health-explanation-item {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 0.8rem;
}


.health-explanation-item.physical {
    background:
    linear-gradient(
        135deg,
        #EFF6FF,
        #FFFFFF
    );
}


.health-explanation-item.nutrition {
    background:
    linear-gradient(
        135deg,
        #ECFDF5,
        #FFFFFF
    );
}


.health-explanation-item.lifestyle {
    background:
    linear-gradient(
        135deg,
        #FFF7ED,
        #FFFFFF
    );
}


.health-timeline-list {

    display: grid;

    gap: 1rem;

    margin-top: 1rem;

}


.health-timeline-card {

    padding: 1rem 1.2rem;

    border-radius: 18px;

    border: 1px solid #E2E8F0;

    background: #FFFFFF;

    box-shadow:
        0 10px 24px
        rgba(15, 23, 42, 0.04);

}


.health-timeline-header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 1rem;

    flex-wrap: wrap;

    margin-bottom: 0.9rem;

}


.health-timeline-date {

    font-size: 0.95rem;

    color: #475569;

    font-weight: 600;

}


.health-timeline-badge {

    display: inline-flex;

    align-items: center;

    padding:
        0.45rem
        0.85rem;

    border-radius: 999px;

    font-size: 0.82rem;

    font-weight: 750;

    white-space: nowrap;

}


.health-timeline-footer {

    display: flex;

    gap: 0.75rem;

    flex-wrap: wrap;

}


.health-timeline-chip {

    display: inline-flex;

    align-items: center;

    gap: 0.35rem;

    padding:
        0.5rem
        0.8rem;

    border-radius: 999px;

    background: rgba(148, 163, 184, 0.12);

    color: #334155;

    font-size: 0.84rem;

    font-weight: 600;

}


.health-timeline-chip strong {

    color: #0F172A;

    font-weight: 750;

}


/* ═══════════════════════════════════════
   Vertical Medical Timeline  (health-vtl-*)
═══════════════════════════════════════ */

.health-vtl-container {
    display: flex;
    flex-direction: column;
    margin-top: 1.2rem;
    padding-bottom: 0.5rem;
}

/* Each row: [rail | card] */
.health-vtl-item {
    display: flex;
    gap: 1.25rem;
    align-items: flex-start;
}

/* ── Left rail: dot + vertical connector ── */
.health-vtl-rail {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    width: 24px;
    padding-top: 0.55rem;
}

.health-vtl-dot {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
    transition: transform 0.2s ease;
}

.health-vtl-dot--latest {
    width: 18px;
    height: 18px;
}

.health-vtl-connector {
    width: 2px;
    flex: 1 1 auto;
    min-height: 1.8rem;
    background: linear-gradient(
        180deg,
        rgba(148, 163, 184, 0.5) 0%,
        rgba(148, 163, 184, 0.18) 100%
    );
    margin-top: 5px;
    margin-bottom: 0;
    border-radius: 999px;
}

/* ── Timeline card ── */
.health-vtl-card {
    flex: 1 1 auto;
    min-width: 0;
    margin-bottom: 1.15rem;
    padding: 1rem 1.25rem;
    border: 1px solid var(--clr-border);
    border-radius: var(--radius-lg);
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(8px);
    box-shadow: var(--shadow-sm);
    transition:
        transform var(--transition-base) var(--ease-spring),
        box-shadow var(--transition-base) ease,
        border-color var(--transition-base) ease;
}

.health-vtl-card:hover {
    transform: translateX(3px);
    box-shadow:
        0 8px 20px -4px rgba(15, 23, 42, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);
}

.health-vtl-card--latest {
    border-width: 1.5px;
    background:
        radial-gradient(circle at 96% 8%, rgba(37, 99, 235, 0.04) 0%, transparent 50%),
        rgba(255, 255, 255, 0.98);
}

/* Card top: date row + category name */
.health-vtl-card-top {
    margin-bottom: 0.75rem;
}

.health-vtl-date-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.35rem;
    flex-wrap: wrap;
}

.health-vtl-date {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748B;
    letter-spacing: 0.01em;
}

.health-vtl-latest-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.12rem 0.55rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    color: #FFFFFF;
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35);
}

.health-vtl-category {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 760;
    letter-spacing: -0.015em;
    line-height: 1.2;
}

/* Meta row: confidence bar + model chip */
.health-vtl-meta-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}

.health-vtl-confidence-block {
    flex: 1 1 120px;
    min-width: 100px;
}

.health-vtl-meta-label {
    font-size: 0.67rem;
    font-weight: 750;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #94A3B8;
    margin-bottom: 0.3rem;
}

.health-vtl-confidence-bar-wrap {
    display: flex;
    align-items: center;
    gap: 0.55rem;
}

.health-vtl-bar-track {
    flex: 1 1 auto;
    height: 5px;
    background: #E2E8F0;
    border-radius: 999px;
    overflow: hidden;
}

.health-vtl-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.health-vtl-confidence-value {
    font-size: 0.8rem;
    font-weight: 760;
    white-space: nowrap;
    font-family: 'Outfit', sans-serif;
}

.health-vtl-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    background: rgba(241, 245, 249, 0.9);
    border: 1px solid rgba(226, 232, 240, 0.8);
    white-space: nowrap;
}

.health-vtl-chip-label {
    font-size: 0.68rem;
    font-weight: 650;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.health-vtl-chip-value {
    font-size: 0.76rem;
    font-weight: 700;
    color: #334155;
    font-family: 'Outfit', sans-serif;
}


/* ═══════════════════════════════════════
   BMI Dashboard Card
═══════════════════════════════════════ */

.health-bmi-card {
    margin-top: 1.4rem;
    padding: 1.55rem 1.7rem 1.2rem;
    border: 1px solid rgba(219, 234, 254, 0.9);
    border-radius: 20px;
    background:
        radial-gradient(circle at 95% 5%, rgba(56, 189, 248, 0.06) 0%, transparent 50%),
        linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
    box-shadow:
        0 4px 18px -4px rgba(15, 23, 42, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
}


/* ── Header row: left col (value) + right col (reference table) ── */
.health-bmi-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.health-bmi-header-left {
    flex: 1 1 auto;
    min-width: 0;
}

.health-bmi-kicker {
    display: block;
    margin-bottom: 0.3rem;
    color: #2563EB;
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Hero row: big number + unit + badge all on one line */
.health-bmi-hero-row {
    display: flex;
    align-items: baseline;
    gap: 0.55rem;
    flex-wrap: wrap;
}

.health-bmi-value {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    color: #0F172A;
    font-size: 3.6rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
}

.health-bmi-unit {
    color: #64748B;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 0.15rem;
    align-self: flex-end;
}

/* Status badge — colours set per-class below */
.health-bmi-badge {
    display: inline-flex;
    align-items: center;
    align-self: center;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 750;
    letter-spacing: 0.03em;
    white-space: nowrap;
    border: 1px solid transparent;
}

.health-bmi-badge.underweight {
    background: #E0F2FE;
    color: #0369A1;
    border-color: rgba(3, 105, 161, 0.18);
}
.health-bmi-badge.normal {
    background: #DCFCE7;
    color: #166534;
    border-color: rgba(22, 101, 52, 0.18);
}
.health-bmi-badge.overweight {
    background: #FEF9C3;
    color: #854D0E;
    border-color: rgba(133, 77, 14, 0.18);
}
.health-bmi-badge.obesity {
    background: #FEE2E2;
    color: #991B1B;
    border-color: rgba(153, 27, 27, 0.18);
}
.health-bmi-badge.age-specific {
    background: #F1F5F9;
    color: #475569;
    border-color: rgba(71, 85, 105, 0.18);
}

.health-bmi-inputs {
    margin-top: 0.5rem;
    color: #64748B;
    font-size: 0.82rem;
}
.health-bmi-inputs strong {
    color: #334155;
    font-weight: 650;
}


/* ── Reference table (right side) ── */
.health-bmi-ref-table {
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    gap: 0.22rem;
    min-width: 160px;
    padding: 0.7rem 0.85rem;
    border-radius: 14px;
    background: rgba(248, 250, 252, 0.9);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.health-bmi-ref-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.6rem;
    padding: 0.28rem 0.45rem;
    border-radius: 8px;
    font-size: 0.73rem;
}

.health-bmi-ref-label {
    font-weight: 600;
    white-space: nowrap;
}

.health-bmi-ref-range {
    font-weight: 500;
    white-space: nowrap;
    opacity: 0.82;
}

.bmi-ref-underweight { background: rgba(224, 242, 254, 0.65); color: #0369A1; }
.bmi-ref-normal      { background: rgba(220, 252, 231, 0.65); color: #166534; }
.bmi-ref-overweight  { background: rgba(254, 249, 195, 0.65); color: #854D0E; }
.bmi-ref-obesity     { background: rgba(254, 226, 226, 0.65); color: #991B1B; }


/* ── Segmented colour scale ── */
.health-bmi-scale-wrap {
    margin-top: 1.35rem;
}

.health-bmi-scale {
    position: relative;
    display: flex;
    height: 12px;
    border-radius: 999px;
    overflow: visible;
    gap: 2px;
}

/* Four coloured segments with proportional widths matching 10–45 range:
   Underweight: 10–18.5  = 8.5/35 ≈ 24%
   Normal:      18.5–25  = 6.5/35 ≈ 19%
   Overweight:  25–30    = 5/35   ≈ 14%
   Obesity:     30–45    = 15/35  ≈ 43%   */
.health-bmi-seg {
    height: 100%;
    border-radius: 999px;
}
.seg-underweight { flex: 24 0 0; background: #38BDF8; }
.seg-normal      { flex: 19 0 0; background: #22C55E; }
.seg-overweight  { flex: 14 0 0; background: #EAB308; }
.seg-obesity     { flex: 43 0 0; background: #EF4444; }

/* Marker */
.health-bmi-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 10;
    pointer-events: none;
}

.health-bmi-marker-tip {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #0F172A;
    border: 3px solid #FFFFFF;
    box-shadow:
        0 0 0 2px #0F172A,
        0 2px 6px rgba(15, 23, 42, 0.3);
}

.health-bmi-scale-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.42rem;
    color: #94A3B8;
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.01em;
}


/* ── Footer notice ── */
.health-bmi-notice {
    display: flex;
    align-items: flex-start;
    gap: 0.45rem;
    margin-top: 1rem;
    padding: 0.6rem 0.85rem;
    border-radius: 10px;
    background: rgba(248, 250, 252, 0.95);
    border: 1px solid rgba(226, 232, 240, 0.7);
    color: #64748B;
    font-size: 0.76rem;
    line-height: 1.5;
}

.health-bmi-notice-icon {
    flex-shrink: 0;
    font-size: 0.82rem;
    color: #94A3B8;
    margin-top: 0.04rem;
}

/* ── Keep old classes inert (referenced nowhere new but harmless) ── */
.health-bmi-title,
.health-bmi-details,
.health-bmi-age-note,
.health-bmi-category { display: none; }



/* ═══════════════════════════════════════
   PDF Report Download Card
═══════════════════════════════════════ */

.health-report-card {
    margin-top: 1.2rem;
    padding: 1.55rem 1.7rem 1.4rem;
    border-radius: 20px;
    border: 1px solid rgba(219, 234, 254, 0.9);
    background:
        radial-gradient(circle at 96% 8%, rgba(37, 99, 235, 0.07) 0%, transparent 45%),
        radial-gradient(circle at 4% 90%, rgba(13, 148, 136, 0.05) 0%, transparent 40%),
        linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
    box-shadow:
        0 4px 18px -4px rgba(15, 23, 42, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);
}


/* ── Header ── */
.health-report-header {
    display: flex;
    align-items: flex-start;
    gap: 1.1rem;
}

.health-report-header-text {
    flex: 1 1 auto;
    min-width: 0;
}

.health-report-icon {
    flex-shrink: 0;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 1px solid rgba(147, 197, 253, 0.5);
    color: #2563EB;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
}

.health-report-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 1.18rem;
    font-weight: 750;
    color: #0F172A;
    letter-spacing: -0.02em;
}

.health-report-ready-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    background: #DCFCE7;
    color: #166534;
    border: 1px solid rgba(22, 101, 52, 0.18);
    font-size: 0.68rem;
    font-weight: 750;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.health-report-subtitle {
    margin-top: 0.25rem;
    color: #64748B;
    font-size: 0.84rem;
    line-height: 1.45;
}

/* ── Feature grid ── */
.health-report-features {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.38rem 1.5rem;
    margin-top: 1.15rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(226, 232, 240, 0.7);
}

.health-report-feature {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: #475569;
    font-weight: 500;
}

.health-report-feature-dot {
    flex-shrink: 0;
    width: 7px;
    height: 7px;
    border-radius: 50%;
}

.dot-blue { background: #3B82F6; }
.dot-teal { background: #14B8A6; }


/* ── Streamlit download button override ── */
div[data-testid="stDownloadButton"] > button[kind="primary"] {
    margin-top: 0.85rem;
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 60%, #3B82F6 100%) !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.78rem 1.4rem !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em !important;
    box-shadow:
        0 4px 14px rgba(37, 99, 235, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

div[data-testid="stDownloadButton"] > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%) !important;
    box-shadow:
        0 8px 24px rgba(37, 99, 235, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stDownloadButton"] > button[kind="primary"]:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
}


/* ── Legacy classes (kept to avoid any breakage) ── */
.health-report-content,
.health-report-content ul,
.health-report-content li,
.health-report-reference { display: none; }



@media (
    max-width: 800px
) {

    .block-container {
        padding-top: 1rem;
    }

    .health-hero {
        padding:
            2rem
            1.35rem;
    }

    .health-hero-title {
        font-size: 2.3rem;
    }

    .health-hero-description {
        font-size: 0.96rem;
    }

    .health-stats {
        grid-template-columns: 1fr;
    }

    .health-stepper {
        grid-template-columns: 1fr;
    }

    .health-stepper-cards {
        grid-template-columns: 1fr;
    }

    .health-progress-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.6rem;
    }

    .health-progress-dots-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.6rem;
    }

    .health-result-meta {
        grid-template-columns: 1fr;
    }

    .health-history-summary {
        grid-template-columns: 1fr;
    }

    .health-detail-grid {
        grid-template-columns: 1fr;
    }

    .health-explanation-grid {
        grid-template-columns: 1fr;
    }

    .health-result-top {
        grid-template-columns: 1fr;
    }

    .health-confidence-card {
        width: 100%;
        min-width: 0;
    }

    .health-confidence-box {
        width: 100%;
    }

    .health-timeline-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .health-timeline-footer {
        flex-direction: column;
        align-items: flex-start;
    }

    .health-vtl-item {
        gap: 0.85rem;
    }

    .health-vtl-rail {
        width: 18px;
    }

    .health-vtl-meta-row {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.6rem;
    }

    .health-bmi-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .health-bmi-ref-table {
        width: 100%;
        min-width: 0;
    }

    .health-bmi-scale-labels {
        font-size: 0.6rem;
    }

    .health-bmi-value {
        font-size: 2.8rem;
    }

}


@media (
    max-width: 520px
) {

    .health-hero {
        border-radius: 22px;
    }

    .health-hero-title {
        font-size: 2rem;
    }

    .health-page-title {
        font-size: 1.55rem;
    }

    .health-result-category {
        font-size: 1.75rem;
    }

}

</style>
"""


def load_app_styles():
    st.html(
        APP_CSS
    )