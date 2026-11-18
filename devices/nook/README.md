# Nook e-reader

## Identify it first
Model number is on the back or under the battery cover.
- **Nook Simple Touch / Glowlight (BNRV300, BNRV350):** the best one to have. Rootable with NookManager from an SD card, runs Android 2.1, has Wi-Fi.
- **Original Nook (2009, BNRV100):** e-ink plus a small color LCD. Harder to repurpose.
- **Later Glowlights / Nook tablets:** newer Android, varies by model.

## Plan: E-ink wall dashboard
1. Root the Nook and keep it plugged in. E-ink only draws power when it refreshes.
2. A server (the Intel Mac mini, a Pi, or a cloud job) renders a PNG of weather, calendar and so on, sized to the screen (600x800).
3. The Nook fetches and shows that image every N minutes.

The panel itself is hard to reuse on its own, because its connectors and driver chips are proprietary. Keep the Nook whole.

## Open questions
- [ ] Find it and get the model number
- [ ] Does it still hold a charge?
