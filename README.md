# EyeGraph (NeurIPS 2024)

EyeGraph: Modularity-aware Spatio Temporal Graph Clustering for Continuous Event-based Eye Tracking

[Paper](https://openreview.net/pdf?id=YxuuzyplFZ) | [Project Page](https://eye-tracking-for-physiological-sensing.github.io/eyegraph/) | [Form for Dataset Access](https://forms.office.com/r/PgHHLxgMNj) | [Supplementary Materials](https://proceedings.neurips.cc/paper_files/paper/2024/file/d9d40ea135f064d9e49e0579e59ad773-Supplemental-Datasets_and_Benchmarks_Track.pdf)

Please fill out the following form to get access to the dataset: [Form Link](https://forms.office.com/r/PgHHLxgMNj)

## Abstract
Continuous tracking of eye movement dynamics plays a significant role in developing a broad spectrum of human-centered applications, such as cognitive skills (visual attention and working memory) modeling, human-machine interaction, biometric user authentication, and foveated rendering. Recently neuromorphic cameras have garnered significant interest in the eye-tracking research community, owing to their sub-microsecond latency in capturing intensity changes resulting from eye movements. Nevertheless, the existing approaches for event-based eye tracking suffer from several limitations: dependence on RGB frames, label sparsity, and training on datasets collected in controlled lab environments that do not adequately reflect real-world scenarios. To address these limitations, in this paper, we propose a dynamic graph-based approach that uses a neuromorphic event stream captured by Dynamic Vision Sensors (DVS) for high-fidelity tracking of pupillary movement. More specifically, first, we present EyeGraph, a large-scale multi-modal near-eye tracking dataset collected using a wearable event camera attached to a head-mounted device from 40 participants -- the dataset was curated while mimicking in-the-wild settings, accounting for varying mobility and ambient lighting conditions. Subsequently, to address the issue of label sparsity, we adopt an unsupervised topology-aware approach as a benchmark. To be specific, (a) we first construct a dynamic graph using Gaussian Mixture Models (GMM), resulting in a uniform and detailed representation of eye morphology features, facilitating accurate modeling of pupil and iris. Then (b) apply a novel topologically guided modularity-aware graph clustering approach to precisely track the movement of the pupil and address the label sparsity in event-based eye tracking. We show that our unsupervised approach has comparable performance against the supervised approaches while consistently outperforming the conventional clustering approaches.

## Overview

<img src="https://github.com/eye-tracking-for-physiological-sensing/eyegraph/blob/main/resources/EyeGraph_overview.png"><br />

## EyeGraph Dataset
To our knowledge, EyeGraph is the only dataset that comprehensively captures eye-tracking data under naturalistic indoor conditions. In below table, we present a comparative summary of EyeGraph vs. four publicly available event-based eye-tracking datasets, highlighting the distinctive attributes and advantages of each. Further, a detailed analysis on EyeGraph is presented in supplementary materials.

| Feature                          | EBV-Eye | EV-Eye | 3ET | 3ET+ | EyeGraph |
|----------------------------------|--------------------------------------|--------------------------|------------------------|---------------------------|------------------|
| Tracking End Goal                | Gaze                                 | Gaze                     | Pupil                  | Pupil                     | Pupil            |
| Representation                   | 2D frame                             | 2D frame                 | 2D frame               | 2D frame                  | Graph            |
| Learning                         | supervised                           | supervised               | supervised             | supervised                | unsupervised     |
| Has Grayscale/RGB Frame Data?    | &check;                         | &check;             | &cross;               | &cross;                  | &check;     |
| Is data from human participants? | &check;                         | &check;             | &cross;               | &check;              | &check;     |
| Is Monocular?                    | &cross;                             | &cross;                 | N/A                    | &check;              | &check;     |
| Is Multi-modal?                  | &check;                         | &check;             | &cross;               | &cross;                 | &check;     |
| Number of participants           | 24                                   | 48                       | N/A                    | 13                        | 40               |
| Is head-movement allowed?        | &cross;                            | &cross;                 | N/A                    | &cross;                  | &check;     |
| Accounts lighting changes?       | &cross;                            | &cross;                | &cross;              | &cross;                  | &check;     |
| Accounts participant mobility?   | &cross;                            | &cross;                | N/A                    | &cross;                  | &check;     |

## Citation

If you find our work useful and/or use in your research work, including the methods, this repository and our dataset, please consider giving a star ⭐ and citing our paper.
```bibtex
@article{bandara2024eyegraph,
  title={EyeGraph: Modularity-aware Spatio Temporal Graph Clustering for Continuous Event-based Eye Tracking},
  author={Bandara, Nuwan and Kandappu, Thivya and Sen, Argha and Gokarn, Ila and Misra, Archan},
  journal={Advances in Neural Information Processing Systems},
  volume={37},
  pages={120366--120380},
  year={2024}
}
```

Please contact Nuwan at pmnsbandara@smu.edu.sg if you have any issues concerning this work. 
