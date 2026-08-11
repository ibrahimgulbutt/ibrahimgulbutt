<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/hero.svg" alt="Ibrahim Gul Butt. I build mobile apps, web apps, desktop apps, Linux internals, cloud platforms and ML pipelines" width="100%">

<p align="center">
  <img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/portrait.svg"
       alt="Ibrahim Gul Butt, rendered as ASCII art" width="400">
</p>

I ship across the whole stack, and I mean the whole thing: a PAM module in Rust that
authenticates your Linux login, a native Android app in Kotlin, a React dashboard, a
zero-knowledge file store, a YOLO segmentation pipeline, and the Kubernetes platform all of
it lands on. Some of it is the day job. Most of it is because the thing should have existed
and didn't.

Site reliability and platform engineering pay the bills: AKS and OKE, Terraform, ArgoCD,
and the pager. The rest of this page is the other half.

Final year of Software Engineering at FAST-NUCES, Lahore. Graduating December 2026.

<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/dashboard.svg"
     alt="Live activity dashboard: contributions per week, commits, repositories, streak and language mix"
     width="100%">

<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/stack.svg" alt="Stack by domain: mobile, web, backend, platform, reliability, systems and ML" width="100%">

## Mobile

|  |  |
|---|---|
| **[Node Mind](https://github.com/ibrahimgulbutt/task_node_map)** · Ionic React, Capacitor<br>Tasks, an infinite mind map canvas and a focus timer in one app. Node based brainstorming that survives being used on a phone. | **[Node Mind, native](https://github.com/ibrahimgulbutt/Node-Mind)** · Kotlin, Android<br>The same idea rebuilt as a native Android app. Gradle KTS, no web view in sight. Worth doing once to feel the difference. |
| **[EcoStay](https://github.com/ibrahimgulbutt/ionic_capacitor_ecostayapp)** · Ionic React, Capacitor<br>A stay booking app with a real Android target wired through Capacitor, not just a responsive website in a shell. | |

## Web

|  |  |
|---|---|
| **[Mermaid Studio](https://github.com/ibrahimgulbutt/diagram_builder)** · Vanilla JS<br>A Mermaid diagram editor that is a single `index.html`. No build step, no backend, 11 templates, live preview, SVG and PNG export at 4×. | **[Encrypted Files](https://github.com/ibrahimgulbutt/Encrypted-files-frontend)** · TypeScript, React<br>The client half of a zero knowledge store: encryption happens in your browser, so the server holds ciphertext and nothing else. [Backend →](https://github.com/ibrahimgulbutt/Encrypted-files-backend) |
| **[indoor-booking](https://github.com/ibrahimgulbutt/indoor-booking)** · React, Vite, Tailwind<br>Booking flow for indoor venues, built on Vite and shipped to Vercel. | **[molecular-3D-Animation](https://github.com/ibrahimgulbutt/molecular-3D-Animation)** · JavaScript<br>Molecules rendered and animated in 3D in the browser, from an era when I mostly wanted to see if I could. |

## Systems and desktop

|  |  |
|---|---|
| **[faceauth](https://github.com/ibrahimgulbutt/faceauth)** · Rust<br>Windows Hello for Linux. A real PAM module (`pam_faceauth` plus a `faceauthd` daemon) that authenticates `sudo`, GDM, SDDM and LightDM from any webcam. One line installer, [architecture written down](https://github.com/ibrahimgulbutt/faceauth/blob/main/ARCHITECTURE.md). | **[sticky-notes-ubuntu](https://github.com/ibrahimgulbutt/sticky-notes-ubuntu)** · Electron, React<br>Sticky notes for the Linux desktop, because every good one I found was macOS only. Ships as a `.deb` on the releases page. |

## Cloud and reliability

<img src="https://raw.githubusercontent.com/ibrahimgulbutt/ibrahimgulbutt/main/assets/pipeline.svg" alt="A deploy moving through commit, build, test and deploy, then landing as healthy pods in production" width="100%">

|  |  |
|---|---|
| **[fastapi-docker-ci](https://github.com/ibrahimgulbutt/fastapi-docker-ci)** · Python, Docker<br>One service, two Dockerfiles: **1.27 GB** naive against **249 MB** done properly. Slim base, discarded build stage, non root, health checked, built and pushed by GitHub Actions. | **[ci-cd-testing](https://github.com/ibrahimgulbutt/ci-cd-testing)** · Kubernetes, Actions<br>Deployment, service and ingress manifests driven by a self hosted Actions runner. The unglamorous plumbing, on purpose. |
| **[Jenkins-minikube-practice-ci-cd](https://github.com/ibrahimgulbutt/Jenkins-minikube-practice-ci-cd)** · Jenkins, Minikube<br>Jenkins into Minikube the long way round, to understand what the managed version is doing for me. | |

## Machine learning

|  |  |
|---|---|
| **[model-training](https://github.com/ibrahimgulbutt/model-training)** · **[model-testing](https://github.com/ibrahimgulbutt/model-testing)** · PyTorch, YOLOv11, OpenCV<br>Car damage segmentation end to end: COCO to YOLOv11 conversion over 10,400 images and 7 damage classes, then a Streamlit app to run the trained weights and look at what they got wrong. | |

<details>
<summary>&nbsp;<b>The older shelf</b>, kept honest about its age</summary>

<br>

- **[maps-visualization](https://github.com/ibrahimgulbutt/maps-visualization)**, **[uml](https://github.com/ibrahimgulbutt/uml)**, **[E-commerce](https://github.com/ibrahimgulbutt/E-commerce)**, **[My-Blog-Page](https://github.com/ibrahimgulbutt/My-Blog-Page)**: earlier browser and Java work, from the learning years.
- **[internship-alpha-bridge](https://github.com/ibrahimgulbutt/internship-alpha-bridge)**: DevOps internship tasks, summer 2025.
- **[Docker_practice_project](https://github.com/ibrahimgulbutt/Docker_practice_project)**, **[rock-paper-scissor](https://github.com/ibrahimgulbutt/rock-paper-scissor)**: exactly what they say.

</details>

## How I work

I like the unglamorous half of this job. Rollbacks that actually roll back. Images that are
small because someone sat down and made them small. Alerts that earn the 3 a.m. they cost you.
The same instinct shows up in the apps. I would rather ship one screen that behaves correctly
offline than five that only work on the demo network.

Most of what's here is meant to be cloned and run, not admired. If a README claims a number,
there is a command underneath it that produces the number. That includes this page. The header
is a hand written SVG in [`assets/`](https://github.com/ibrahimgulbutt/ibrahimgulbutt/blob/main/assets),
generated by [`tools/build.py`](https://github.com/ibrahimgulbutt/ibrahimgulbutt/blob/main/tools/build.py):
theme aware from a single file, animation switched off for anyone whose OS asks for reduced
motion, and dependent on exactly zero third party services that could rate limit it into a
broken image.

<br>

<sub>Lahore, Pakistan · ibrahimgulbutt242@gmail.com</sub>
