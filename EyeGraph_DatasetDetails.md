# Title: EyeGraph: Modularity-aware Spatio Temporal Graph Clustering for Continuous Event-based Eye Tracking

# Project Home Page: https://eye-tracking-for-physiological-sensing.github.io/eyegraph/

# Abstract
Continuous tracking of eye movement dynamics plays a significant role in developing a broad spectrum of human-centered applications, such as cognitive skills (visual attention and working memory) modeling, human-machine interaction, biometric user authentication, and foveated rendering. Recently neuromorphic cameras have garnered significant interest in the eye-tracking research community, owing to their sub-microsecond latency in capturing intensity changes resulting from eye movements. Nevertheless, the existing approaches for event-based eye tracking suffer from several limitations: dependence on RGB frames, label sparsity, and training on datasets collected in controlled lab environments that do not adequately reflect real-world scenarios. To address these limitations, in this paper, we propose a dynamic graph-based approach that uses a neuromorphic event stream captured by Dynamic Vision Sensors (DVS) for high-fidelity tracking of pupillary movement. More specifically, first, we present EyeGraph, a large-scale multi-modal near-eye tracking dataset collected using a wearable event camera attached to a head-mounted device from 40 participants -- the dataset was curated while mimicking in-the-wild settings, accounting for varying mobility and ambient lighting conditions. Subsequently, to address the issue of label sparsity, we adopt an unsupervised topology-aware approach as a benchmark. To be specific, (a) we first construct a dynamic graph using Gaussian Mixture Models (GMM), resulting in a uniform and detailed representation of eye morphology features, facilitating accurate modeling of pupil and iris. Then (b) apply a novel topologically guided modularity-aware graph clustering approach to precisely track the movement of the pupil and address the label sparsity in event-based eye tracking. We show that our unsupervised approach has comparable performance against the supervised approaches while consistently outperforming the conventional clustering approaches [1].

# Background 
Fine-grained, high-frequency eye tracking is increasingly of interest as an enabler of a wide variety of applications, such as biometric user authentication [2], foveated rendering for augmented and virtual reality [3], and monitoring of cognitive attention/overload [4]. However, rapid and intricate eye movements (with pupillary acceleration reaching values as high as 24, 000 degree/s2 [5]), such as fixations (moments when the eyes are stationary and focused on a particular point), saccades (quick movements of both eyes between fixation points in the same direction), and microsaccades (small involuntary eye movements within fixation points) are difficult to capture with conventional RGB cameras due to their poor temporal resolution, susceptibility to motion blur, and constrained capability to accurately detect and track pupils under low lighting conditions. In this work, we explore the possibility of using Neuromorphic event cameras as an alternative to traditional RGB-based eye tracking. Neuromorphic vision sensors capture changes in the visual scene asynchronously, only recording data when a significant event occurs, leading to a more efficient, high-frequency, and finer-grained depiction of eye movement dynamics [1].

To our knowledge, EyeGraph is the only dataset that comprehensively captures eye-tracking data under naturalistic indoor conditions. In below table, we present a comparative summary of EyeGraph vs. four publicly available event-based eye-tracking datasets, highlighting the distinctive attributes and advantages of each. Further, a detailed analysis on EyeGraph is presented in supplementary materials [1].

| Feature                          | EBV-Eye [5] | EV-Eye [6] | 3ET [7] | 3ET+ [8] | EyeGraph |
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

# Methods
During the data collection process, the participants wear a custom-built head-mounted device (HMD) equipped with a DAVIS346 camera. The HMD was secured around the forehead using a Velcro fastener. The camera is positioned adjacent to the right eye, while the participants are directed to track the visual stimuli using their left eye. To elicit natural eye movements, the visual stimulus appears at the top left corner of the screen and then moves continuously in random directions. To guide the gaze movement of the participants, we displayed the visual stimulus on a 1920 × 1080, 23.8-inch monitor. The distance between the monitor and the participant varied between 45cm and 50cm, resulting in a field of view between 56◦ × 34◦ and 62◦ × 37◦, except when the participant moves freely. To collect reference for cross-modal investigations, the participants wear the off-the-shelf Pupil-Core eye tracker at which their gaze is guided by replaying an identical visual stimulus. To record eye-tracking data for a wider range of practical and in-the-wild conditions, we use three experimental setups: (i) conventional lab settings – the participant is seated in an office environment (default illuminance) while watching the visual stimulus on a screen. The participants can move their heads without maintaining a fixed/rigid posture, (ii) changing ambient 4 illuminance: the experiment is repeated both under regular lighting (348 Lux) and under lower illuminance (24 Lux), with the corresponding near-eye Lux values being 65 and 8 Lux, respectively, and (iii) user mobility – the participants are asked to move around freely within the lab while carrying a laptop (3024 × 1964, 14-inch screen) that displays the visual stimuli, resulting in natural head and body movement [1].

# Participant Pool
Our participant pool consists of 40 participants, including 28 males and 12 females, representing diverse ethnic backgrounds (ages ranging from 21 to 32 years, μ = 26.08 years and σ = 2.99). Our institution’s IRB approved our data collection and the participants gave their written informed consent to release the raw data collected [1]. 

# Dataset Instructions 
As mentioned above, Our EyeGraph dataset is a multi-modal, near-eye and mobile event-based eye tracking dataset which provides both raw event data and RGB frames, collected from 40 participants under three experimental setups: (1) conventional lab settings, (2) changing ambient illuminance and (3) user mobility, to capture event-based eye tracking in a wider range of practical and in-the-wild conditions.  

## The file structure in the dataset is shown as follows:
### Under conventional lab settings
```
EyeGraph_Dataset/
|-- 1
|   |-- 1_000.aedat4
|   |-- 1_001.aedat4
|   |-- 1 
|   |   |-- 1_000
|   |   |   |-- exports
|   |   |   |   |-- 000
|   |   |   |   |   |-- export_info.csv
|   |   |   |   |   |-- pupil_positions.csv
|   |   |   |   |   |-- gaze_positions.csv
|   |   |   |   |   |-- fixations.csv
|   |   |   |   |   |-- world_timestamps.csv
|   |   |   |   |   |-- ...
|   |   |   |-- offline_data
|   |   |   |   |-- tokens
|   |   |   |   |-- fixations.meta
|   |   |   |   |-- ...
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- eye0_timestamps.npy
|   |   |   |-- eye0_lookup.npy
|   |   |   |-- eye1.mp4
|   |   |   |-- eye1.intrinsics
|   |   |   |-- eye1_timestamps.npy
|   |   |   |-- eye1_lookup.npy
|   |   |   |-- blinks.pldata
|   |   |   |-- blinks_timestamps.npy
|   |   |   |-- fixations.pldata
|   |   |   |-- fixations_timestamps.npy
|   |   |   |-- gaze.pldata
|   |   |   |-- gaze_timestamps.npy
|   |   |   |-- notify.pldata
|   |   |   |-- notify_timestamps.npy
|   |   |   |-- pupil.pldata
|   |   |   |-- pupil_timestamps.npy
|   |   |   |-- world.intrinsics
|   |   |   |-- world_lookup.npy
|   |   |-- 1_001
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- ...
|-- 2
|   |-- 2_000.aedat4
|   |-- 2_001.aedat4
|   |-- 2
|   |   |-- 2_000
|   |   |   |-- ...
|   |   |-- 2_001
|   |   |   |-- ...
|-- ...
|-- 40
|   |-- 40_000.aedat4
|   |-- 40_001.aedat4
|   |-- 40
|   |   |-- 40_000
|   |   |   |-- ...
|   |   |-- 40_001
|   |   |   |-- ...
```
### Under changing ambient illuminance
```
EyeGraph_Dataset/
|-- 41
|   |-- 5.aedat4
|   |-- 5L.aedat4
|   |-- annotations_5L_dvSave.json
|   |-- 41 
|   |   |-- 5_000
|   |   |   |-- exports
|   |   |   |   |-- 000
|   |   |   |   |   |-- ...
|   |   |   |-- offline_data
|   |   |   |   |-- ...
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- ...
|   |   |-- 5L_000
|   |   |   |-- exports
|   |   |   |   |-- 000
|   |   |   |   |   |-- ...
|   |   |   |-- offline_data
|   |   |   |   |-- ...
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- ...
|-- ...
|-- 45
|   |-- 20.aedat4
|   |-- 20L.aedat4
|   |-- annotations_20L_dvSave.json
|   |-- 45
|   |   |-- ...
```
### Under user mobility
```
EyeGraph_Dataset/
|-- 46
|   |-- 5.aedat4
|   |-- 5M.aedat4
|   |-- annotations_5M_dvSave.json
|   |-- 46 
|   |   |-- 5_001
|   |   |   |-- exports
|   |   |   |   |-- 000
|   |   |   |   |   |-- ...
|   |   |   |-- offline_data
|   |   |   |   |-- ...
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- ...
|   |   |-- 5M_001
|   |   |   |-- exports
|   |   |   |   |-- 000
|   |   |   |   |   |-- ...
|   |   |   |-- offline_data
|   |   |   |   |-- ...
|   |   |   |-- eye0.mp4
|   |   |   |-- eye0.intrinsics
|   |   |   |-- ...
|-- ...
|-- 50
|   |-- 20.aedat4
|   |-- 20M.aedat4
|   |-- annotations_20M_dvSave.json
|   |-- 50
|   |   |-- ...
```

## Folder Name Format
For ease of identification, the folders in root directory (i.e., "EyeGraph_Dataset") are called "parent folders" and the folders within parent folders are called "child folders". The parent folders are named by considering each folder as a new data point and thus, through a numerical value [data_point_num] (i.e. 1, 2, ..., 50).

Under each parent folder in conventional lab settings, there are two event files with extension: .aedat4 (named as [subject_id]_[session_id].aedat4), each corresponding to four minutes of eye movement recordings as described in the paper, and a child folder (named as [subject_id]) containing Pupil-Core recordings. The event recordings include (1) event streams, (2) gray-scale image frames recorded at about 30FPS, (3) inertial sensor measurements and (4) external trigger data. As shown in above file structures, the child folder (containing the Pupil-Core data) has two sub-folders (named as [subject_id]_[session_id]) each corresponding to two recording sessions as described in the paper, and consist of rich collection of data including, but not limited to, eye movement videos, pupil data, gaze estimation data, fixation and blinks data and world view data.

The file structure under ambient light illuminance and user mobility follows the following naming convention:
- Two event files in parent folder with extension: .aedat4, named as [subject_id].aedat4 for the default recording (i.e., either default lighting for ambient light illuminance setting or default seating condition for user mobility setting) and [subject_id][X] for in-the-wild recording (i.e., "L" for changing lighting condition and "M" for user mobility condition). 
- The child folder within parent folder (named as [data_point_num]) has two sub-folders for default recording (named as [subject_id]_[session_id]) and in-the-wild recording (named as [subject_id][X]_[session_id]). Each sub-folder has the corresponding Pupil-Core data as described above.
- One annotation file (named as annotations_[subject_id][X]_dvSave.json) which contains the ground-truth for pupil coordinates for the corresponding in-the-wild event recording. 

# Ethics Statement
Our institution’s IRB approved our data collection and the participants gave their written informed consent to release the raw data collected. 
 
# Acknowledgements

This work was supported by both the Ministry of Education (MOE) Academic Research Fund (AcRF) Tier 1 grant (Grant ID: 22-SIS-SMU-044), and by the National Research Foundation, Prime Minister’s Office, Singapore under its NRF Investigatorship grant (NRF-NRFI05- 2019-0007). Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not reflect the views of the National Research Foundation, Singapore.

# Conflicts of Interest

The author(s) have no conflicts of interest to declare.

# References
[1] Bandara N, Kandappu T, Sen A, Gokarn I, Misra A. EyeGraph: Modularity-aware Spatio Temporal Graph Clustering for Continuous Event-based Eye Tracking. Advances in Neural Information Processing Systems. 2024 Dec 16;37:120366-80

[2] A. Sen, N. Bandara, I. Gokarn, T. Kandappu, and A. Misra. EyeTrAES: fine-grained, low-latency eye tracking via adaptive event slicing. arXiv preprint arXiv:2409.18813, 2024

[3] J. Kim, Y. Jeong, M. Stengel, K. Aksit, R. A. Albert, B. Boudaoud, T. Greer, J. Kim, W. Lopes, Z. Majercik, et al. Foveated AR: dynamically-foveated augmented reality display. ACM Trans. Graph., 38(4):99–1, 2019

[4] A. T. Duchowski, K. Krejtz, I. Krejtz, C. Biele, A. Niedzielska, P. Kiefer, M. Raubal, and I. Giannopoulos. The index of pupillary activity: Measuring cognitive load vis-à-vis task difficulty with pupil oscillation. In Proceedings of the 2018 CHI conference on human factors in computing systems, pages 1–13, 2018

[5] A. N. Angelopoulos, J. N. Martel, A. P. Kohli, J. Conradt, and G. Wetzstein. Event-based near-eye gaze tracking beyond 10,000 Hz. IEEE Transactions on Visualization and Computer Graphics, 27(5):2577–2586, 2021

[6] G. Zhao, Y. Yang, J. Liu, N. Chen, Y. Shen, H. Wen, and G. Lan. EV-Eye: Rethinking high-frequency eye tracking through the lenses of event cameras. Advances in Neural Information Processing Systems, 36, 2024

[7] Q. Chen, Z. Wang, S.-C. Liu, and C. Gao. 3ET: Efficient event-based eye tracking using a change-based convlstm network. In 2023 IEEE Biomedical Circuits and Systems Conference (BioCAS), pages 1–5. IEEE, 2023

[8] Z. Wang, C. Gao, Z. Wu, M. V. Conde, R. Timofte, S.-C. Liu, Q. Chen, Z.-j. Zha, W. Zhai, H. Han, et al. Event-based eye tracking. AIS 2024 challenge survey. arXiv preprint arXiv:2404.11770, 2024
