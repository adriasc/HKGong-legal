# Source for the published starter guide

The public download at `assets/hkgong-cantonese-starter-guide.pdf` is the approved
21-page guide dated 11 October 2026. Its editable source is kept in the adjacent
HKGong project at:

`../CantoneseCoach-HKGong/marketing/creativitats/2026-10-11-starter-guide-redesign/`

Edit `source/content_final.json` for vocabulary and patterns, and
`source/build_final.py` for layout and prose. The illustrations and logo are in
`source/assets/`. Run the builder and `source/verify.py` there, then review all
rendered pages before replacing the public PDF. The approved output is
`HKGong_Cantonese_Starter_Guide_FINAL_v02.pdf`, SHA-256
`bcf285516bac62a9e58da734a5bc669c108638ccf7c5557b095952ff42c9e023`.

`generate_starter_guide.py` in this repository is the former 12-page generator.
Its output now has a separate legacy filename so it cannot overwrite the
published download accidentally.
