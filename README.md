<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/hero.svg" alt="Ibrahim Gul Butt — Site Reliability / DevOps, Lahore, Pakistan" width="100%">

### What I actually do

I run Kubernetes platforms for a living — AKS and OKE, wired together with Terraform,
delivered by ArgoCD, and watched closely enough that I usually know before the alert does.
The day job is the pager, the rollback, the postmortem.

The rest of what's here is what I write when nobody assigned it: a PAM module in Rust
because Linux deserved face unlock, an encrypted file store that cannot read your files,
a Mermaid editor that is one HTML file. I build the thing when the thing should exist.

Final year of Software Engineering at FAST-NUCES. Graduating December 2026.

<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/stack.svg" alt="Stack: platform, delivery, reliability, application" width="100%">

### Things I've built

|  |  |
|---|---|
| **[faceauth](https://github.com/ibrahimgulbutt/faceauth)** · Rust<br>Windows Hello for Linux. A PAM module that authenticates `sudo`, GDM, SDDM and LightDM from any webcam. I wanted it, it didn't exist, so it exists now. | **[fastapi-docker-ci](https://github.com/ibrahimgulbutt/fastapi-docker-ci)** · Python, Docker<br>One service, two Dockerfiles: **1.27 GB** naive against **249 MB** done properly — slim base, discarded build stage, non-root, health-checked, shipped by Actions. |
| **[Encrypted Files](https://github.com/ibrahimgulbutt/Encrypted-files-backend)** · FastAPI, Supabase<br>Zero-knowledge storage. Encryption happens in the browser; the server never holds a plaintext byte or a key — by construction, not by policy. [Frontend →](https://github.com/ibrahimgulbutt/Encrypted-files-frontend) | **[sticky-notes-ubuntu](https://github.com/ibrahimgulbutt/sticky-notes-ubuntu)** · Electron, React<br>Sticky notes for the Linux desktop, because every good one I found was macOS-only. Ships as a `.deb` on the releases page. |
| **[diagram_builder](https://github.com/ibrahimgulbutt/diagram_builder)** · Vanilla JS<br>A Mermaid editor that is a single `index.html`. No build step, no backend, live preview, SVG and PNG export at 4×. | **[Node Mind](https://github.com/ibrahimgulbutt/task_node_map)** · Ionic, TypeScript<br>Tasks, mind maps and a focus timer in one mobile app — built during a stretch of trying to think and ship at the same time. |

<details>
<summary>&nbsp;<b>More</b> — CI/CD practice, ML, and the older shelf</summary>

<br>

- **[Jenkins-minikube-practice-ci-cd](https://github.com/ibrahimgulbutt/Jenkins-minikube-practice-ci-cd)** — Jenkins into Minikube, the long way round, on purpose.
- **[model-training](https://github.com/ibrahimgulbutt/model-training)** · **[model-testing](https://github.com/ibrahimgulbutt/model-testing)** — COCO → YOLOv11 segmentation for car damage detection: 10,400 images, 7 damage classes.
- **[faceauth/ARCHITECTURE.md](https://github.com/ibrahimgulbutt/faceauth/blob/main/ARCHITECTURE.md)** — how `pam_faceauth`, the `faceauthd` daemon and the core crate actually fit together.
- **[molecular-3D-Animation](https://github.com/ibrahimgulbutt/molecular-3D-Animation)**, **[maps-visualization](https://github.com/ibrahimgulbutt/maps-visualization)**, **[uml](https://github.com/ibrahimgulbutt/uml)** — earlier browser experiments, kept honest about their age.

</details>

### How I work

I like the unglamorous half of this job. Rollbacks that actually roll back. Images that are
small because someone sat down and made them small. Alerts that earn the 3 a.m. they cost you.

Most of what's here is meant to be cloned and run, not admired — if a README claims a number,
there is a command underneath it that produces the number. That includes this page: the header
above is a hand-written SVG in [`assets/`](https://github.com/ibrahimgulbutt/ibrahimgulbutt/blob/main/assets), built by [`tools/build.py`](https://github.com/ibrahimgulbutt/ibrahimgulbutt/blob/main/tools/build.py),
theme-aware, motion-reduced when you ask it to be, and dependent on exactly zero third-party
services that could rate-limit it into a broken image.

<br>

<sub>Lahore, Pakistan · ibrahimgulbutt242@gmail.com</sub>
