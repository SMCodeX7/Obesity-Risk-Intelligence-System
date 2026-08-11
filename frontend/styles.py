import streamlit as st


APP_CSS = """
<style>

/* ==========================================================
   OBESITY RISK INTELLIGENCE SYSTEM
   Healthcare UI Design System
========================================================== */


/* ----------------------------------------------------------
   MAIN APPLICATION
---------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(
            circle at 88% 2%,
            rgba(56, 189, 248, 0.07),
            transparent 28rem
        ),
        radial-gradient(
            circle at 8% 18%,
            rgba(15, 139, 141, 0.045),
            transparent 24rem
        ),
        #F8FAFC;
}


/* ----------------------------------------------------------
   PAGE CONTAINER
---------------------------------------------------------- */

.block-container {
    max-width: 1180px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}


/* ----------------------------------------------------------
   HERO
---------------------------------------------------------- */

.health-hero {
    position: relative;
    overflow: hidden;

    padding: 2.8rem 3rem;

    border: 1px solid #DBEAFE;
    border-radius: 28px;

    background:
        radial-gradient(
            circle at 92% 12%,
            rgba(56, 189, 248, 0.14),
            transparent 18rem
        ),
        radial-gradient(
            circle at 80% 100%,
            rgba(15, 139, 141, 0.08),
            transparent 20rem
        ),
        linear-gradient(
            135deg,
            #FFFFFF 0%,
            #F8FBFF 48%,
            #EFF6FF 100%
        );

    box-shadow:
        0 20px 55px
        rgba(15, 23, 42, 0.055);
}


.health-hero::after {
    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    right: -90px;
    bottom: -130px;

    border-radius: 50%;

    border:
        42px solid
        rgba(37, 99, 235, 0.035);
}


/* ----------------------------------------------------------
   HERO BADGE
---------------------------------------------------------- */

.health-eyebrow {
    display: inline-flex;

    align-items: center;

    gap: 0.55rem;

    padding:
        0.42rem
        0.8rem;

    margin-bottom: 1.25rem;

    border-radius: 999px;

    border:
        1px solid #BFDBFE;

    background:
        rgba(
            255,
            255,
            255,
            0.88
        );

    color: #1D4ED8;

    font-size: 0.73rem;
    font-weight: 750;

    letter-spacing: 0.075em;
    text-transform: uppercase;
}


.health-eyebrow-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #0F8B8D;

    box-shadow:
        0 0 0 5px
        rgba(15, 139, 141, 0.10);
}


/* ----------------------------------------------------------
   HERO TYPOGRAPHY
---------------------------------------------------------- */

.health-hero-title {
    max-width: 780px;

    margin: 0;

    color: #0F172A;

    font-size:
        clamp(
            2.35rem,
            5vw,
            4rem
        );

    line-height: 1.04;

    letter-spacing: -0.052em;

    font-weight: 780;
}


.health-hero-title span {
    color: #2563EB;
}


.health-hero-description {
    max-width: 720px;

    margin:
        1.25rem
        0
        0;

    color: #475569;

    font-size: 1.03rem;

    line-height: 1.75;
}


/* ----------------------------------------------------------
   HERO STATISTICS
---------------------------------------------------------- */

.health-stats {
    display: grid;

    grid-template-columns:
        repeat(
            3,
            minmax(0, 1fr)
        );

    gap: 0.8rem;

    max-width: 760px;

    margin-top: 2rem;
}


.health-stat {
    padding:
        1rem
        1.15rem;

    border: 1px solid
        rgba(
            148,
            163,
            184,
            0.22
        );

    border-radius: 18px;

    background:
        rgba(
            255,
            255,
            255,
            0.78
        );

    backdrop-filter:
        blur(8px);
}


.health-stat-value {
    display: block;

    color: #0F172A;

    font-size: 1.25rem;

    font-weight: 760;

    letter-spacing: -0.025em;
}


.health-stat-label {
    display: block;

    margin-top: 0.18rem;

    color: #64748B;

    font-size: 0.72rem;

    font-weight: 650;

    letter-spacing: 0.055em;

    text-transform: uppercase;
}


/* ----------------------------------------------------------
   PAGE SECTION HEADER
---------------------------------------------------------- */

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


/* ----------------------------------------------------------
   ASSESSMENT PROGRESS
---------------------------------------------------------- */

.health-stepper {
    display: grid;

    grid-template-columns:
        repeat(
            3,
            minmax(0, 1fr)
        );

    gap: 0.7rem;

    margin:
        1.3rem
        0
        1.4rem;
}


.health-step {
    display: flex;

    align-items: center;

    gap: 0.7rem;

    padding:
        0.82rem
        0.95rem;

    border: 1px solid #E2E8F0;

    border-radius: 17px;

    background: #FFFFFF;

    transition:
        border-color 0.2s ease,
        background 0.2s ease;
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

    flex:
        0
        0
        31px;

    border-radius: 50%;

    background: #F1F5F9;

    color: #64748B;

    font-size: 0.78rem;

    font-weight: 750;
}


.health-step.active
.health-step-number {
    background: #2563EB;
    color: #FFFFFF;
}


.health-step.complete
.health-step-number {
    background: #CCFBF1;
    color: #0F766E;
}


.health-step-name {
    color: #475569;

    font-size: 0.83rem;

    font-weight: 650;
}


.health-step.active
.health-step-name {
    color: #1D4ED8;
}


.health-step.complete
.health-step-name {
    color: #0F766E;
}


/* ----------------------------------------------------------
   INFORMATION CARD
---------------------------------------------------------- */

.health-info-card {
    padding:
        1.05rem
        1.2rem;

    margin-bottom: 1.15rem;

    border: 1px solid #DBEAFE;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #FFFFFF,
            #F8FBFF
        );
}


.health-info-icon {
    display: inline-flex;

    align-items: center;
    justify-content: center;

    width: 31px;
    height: 31px;

    margin-bottom: 0.7rem;

    border-radius: 10px;

    background: #EFF6FF;

    color: #2563EB;

    font-size: 0.85rem;

    font-weight: 800;
}


.health-info-title {
    color: #0F172A;

    font-size: 0.92rem;

    font-weight: 730;
}


.health-info-text {
    max-width: 760px;

    margin-top: 0.28rem;

    color: #64748B;

    font-size: 0.84rem;

    line-height: 1.65;
}


/* ----------------------------------------------------------
   CONTENT CARD
---------------------------------------------------------- */

.health-card {
    padding: 1.4rem;

    border: 1px solid #E2E8F0;

    border-radius: 22px;

    background: #FFFFFF;

    box-shadow:
        0 10px 30px
        rgba(
            15,
            23,
            42,
            0.035
        );
}


/* ----------------------------------------------------------
   RESULT CARD
   Used more extensively during checkpoint 2
---------------------------------------------------------- */

.health-result-card {
    padding: 1.5rem;

    border: 1px solid #BFDBFE;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #FFFFFF,
            #F8FBFF
        );
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


/* ----------------------------------------------------------
   SUBTLE HEALTHCARE NOTICE
---------------------------------------------------------- */

.health-notice {
    padding:
        0.9rem
        1rem;

    border:
        1px solid #CFFAFE;

    border-radius: 16px;

    background: #ECFEFF;

    color: #155E75;

    font-size: 0.82rem;

    line-height: 1.55;
}


/* ----------------------------------------------------------
   SIDEBAR BRAND
---------------------------------------------------------- */

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


/* ----------------------------------------------------------
   STATUS DOT
---------------------------------------------------------- */

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


/* ----------------------------------------------------------
   FOOTER
---------------------------------------------------------- */

.health-footer {
    padding-top: 1.4rem;

    margin-top: 2.5rem;

    border-top:
        1px solid #E2E8F0;

    color: #94A3B8;

    font-size: 0.77rem;

    line-height: 1.65;
}


/* ----------------------------------------------------------
   RESPONSIVE
---------------------------------------------------------- */

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

}

</style>
"""


def load_app_styles():
    st.html(
        APP_CSS
    )