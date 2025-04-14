import os

import numpy as np
import pandas as pd
import seaborn as sns
# sns.set(context="notebook", style="whitegrid", font_scale=1.2)
import csv

import matplotlib.pyplot as plt
import matplotlib.colors as colors

index = "10" #str(7)

exported_gaze_file = f"/content/{index}_gaze_positions.csv"

exported_gaze = pd.read_csv(exported_gaze_file) #.dropna()
exported_gaze.info(verbose=True)

exported_gaze.gaze_point_3d_z
negative_z_mask = exported_gaze.gaze_point_3d_z < 0
negative_z_values = exported_gaze.loc[negative_z_mask,["gaze_point_3d_z"]]
exported_gaze.loc[negative_z_mask, ["gaze_point_3d_z"]] = negative_z_values * -1

def cart_to_spherical(data, apply_rad2deg=False):
    x = data.gaze_point_3d_x
    y = data.gaze_point_3d_y
    z = data.gaze_point_3d_z
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arccos(y / r)  # for elevation angle defined from Z-axis down
    psi = np.arctan2(z, x)

    if apply_rad2deg:
        theta = np.rad2deg(theta)
        psi = np.rad2deg(psi)

    return r, theta, psi

def sphere_pos_over_time(ts, data, unit="radians"):
    for key, values in data.items():
        sns.lineplot(x=ts, y=values, label=key)
    plt.xlabel("time [sec]")
    plt.ylabel(unit)
    plt.legend()

def sphere_pos(r, theta, psi, unit="radians"):
    # print(r.min(), r.max())
    norm = colors.LogNorm(vmin=r.min(), vmax=r.max())
    points = plt.scatter(
        theta,
        psi,
        c=r,
        alpha=0.5,
        cmap="cubehelix",
        norm=norm,
    )
    cbar = plt.colorbar(points)
    cbar.ax.set_ylabel("distance [mm]", rotation=270, fontsize = 14)
    cbar.ax.get_yaxis().labelpad = 15
    plt.xlabel(f"$\\theta$ [{unit[:3]}]", fontsize=18)
    plt.ylabel(f"$\psi$ [{unit[:3]}]", fontsize=18)
    plt.tick_params(axis='both', which='major', labelsize=14)

r, theta, psi = cart_to_spherical(exported_gaze, apply_rad2deg=True)
# print(r)

# plt.figure(figsize=(16, 4))

# plt.subplot(1, 2, 1)
# sphere_pos_over_time(
#     exported_gaze.gaze_timestamp,
#     data={"theta": theta, "psi": psi},
#     unit="degrees"
# )

# plt.subplot(1, 2, 2)
# sphere_pos(r, theta, psi, unit="degrees")

# plt.tight_layout()

# # Create first plot
# fig1, ax1 = plt.subplots(figsize=(8, 6))
# sphere_pos_over_time(
#     exported_gaze.gaze_timestamp,
#     data={"$\theta$": theta, "$\psi$": psi},
#     unit="deg"
# )
# ax1.set_xlabel('Time', fontsize=14)
# ax1.set_ylabel('Angle (deg)', fontsize=14)
# ax1.tick_params(axis='both', which='major', labelsize=12)
# fig1.tight_layout()

# # Save or show the first figure
# plt.show()

# Create second plot
fig2, ax2 = plt.subplots(figsize=(8, 6))
sphere_pos(r, theta, psi, unit="degrees")
# ax2.set_xlabel('$\theta$ (deg)', fontsize=14)
# ax2.set_ylabel('$\psi$ (deg)', fontsize=14)
# ax2.tick_params(axis='both', which='major', labelsize=12)
fig2.tight_layout()

plt.savefig(f'{index}_degrees.jpg', dpi=300)

# Save or show the second figure
plt.show()


for index in range(1, 41):
  exported_gaze_file = os.path.join("./eye_tracking_user_study/gaze_positions", f"{str(index)}_gaze_positions.csv")
  exported_gaze = pd.read_csv(exported_gaze_file) #.dropna()
  # exported_gaze.info(verbose=True)
  exported_gaze.gaze_point_3d_z
  negative_z_mask = exported_gaze.gaze_point_3d_z < 0
  negative_z_values = exported_gaze.loc[negative_z_mask,["gaze_point_3d_z"]]
  exported_gaze.loc[negative_z_mask, ["gaze_point_3d_z"]] = negative_z_values * -1
  r, theta, psi = cart_to_spherical(exported_gaze, apply_rad2deg=True)

  fig2, ax2 = plt.subplots(figsize=(8, 6))
  sphere_pos(r, theta, psi, unit="degrees")
  fig2.tight_layout()
  plt.savefig(f'./gaze_spatial_graphs/{str(index)}_degrees.jpg', dpi=300)
  plt.show()

"""calculate Gaze Velocity"""

squared_theta_diff = np.diff(theta) ** 2
squared_psi_diff = np.diff(psi) ** 2
deg_diff = np.sqrt(squared_theta_diff + squared_psi_diff)
ts_diff = np.diff(exported_gaze.gaze_timestamp)
deg_per_sec = deg_diff / ts_diff

"""Gaze Velocity"""

time = exported_gaze.gaze_timestamp[:-1] - exported_gaze.gaze_timestamp.iloc[0]

# plt.figure(figsize=(16, 4))

# plt.subplot(1, 2, 1)
# sphere_pos_over_time(time, {"gaze velocity": deg_per_sec}, unit="deg/sec")
# plt.title("Gaze velocity over time")

# plt.subplot(1, 2, 2)
# plt.hist(deg_per_sec, bins=np.logspace(-1, np.log10(500), 50))
# plt.title("Gaze velocity histogram")
# plt.xlabel("Gaze velocity [deg/sec]")

fig1, ax1 = plt.subplots(figsize=(8, 6))
plt.hist(deg_per_sec, bins=np.logspace(-1, np.log10(500), 50))
# plt.title("Gaze velocity histogram")
# plt.xlabel("Gaze velocity [deg/sec]")
ax1.set_xlabel('Gaze velocity [deg/sec]', fontsize=18)
ax1.set_ylabel('Count', fontsize=18)
ax1.tick_params(axis='both', which='major', labelsize=14)
fig1.tight_layout()
plt.savefig(f'./{str(index)}_hist.jpg', dpi=300)

# Save or show the first figure
plt.show()

for index in range(1, 41):
  exported_gaze_file = os.path.join("./eye_tracking_user_study/gaze_positions", f"{str(index)}_gaze_positions.csv")
  exported_gaze = pd.read_csv(exported_gaze_file) #.dropna()
  # exported_gaze.info(verbose=True)
  exported_gaze.gaze_point_3d_z
  negative_z_mask = exported_gaze.gaze_point_3d_z < 0
  negative_z_values = exported_gaze.loc[negative_z_mask,["gaze_point_3d_z"]]
  exported_gaze.loc[negative_z_mask, ["gaze_point_3d_z"]] = negative_z_values * -1
  r, theta, psi = cart_to_spherical(exported_gaze, apply_rad2deg=True)

  # fig2, ax2 = plt.subplots(figsize=(8, 6))
  # sphere_pos(r, theta, psi, unit="degrees")
  # fig2.tight_layout()
  # plt.savefig(f'/content/gaze_spatial_graphs/{str(index)}_degrees.jpg', dpi=300)
  # plt.show()

  squared_theta_diff = np.diff(theta) ** 2
  squared_psi_diff = np.diff(psi) ** 2
  deg_diff = np.sqrt(squared_theta_diff + squared_psi_diff)
  ts_diff = np.diff(exported_gaze.gaze_timestamp)
  deg_per_sec = deg_diff / ts_diff

  time = exported_gaze.gaze_timestamp[:-1] - exported_gaze.gaze_timestamp.iloc[0]

  fig1, ax1 = plt.subplots(figsize=(8, 6))
  plt.hist(deg_per_sec, bins=np.logspace(-1, np.log10(500), 50))
  # plt.title("Gaze velocity histogram")
  # plt.xlabel("Gaze velocity [deg/sec]")
  ax1.set_xlabel('Gaze velocity [deg/sec]', fontsize=18)
  ax1.set_ylabel('Count', fontsize=18)
  ax1.tick_params(axis='both', which='major', labelsize=14)
  fig1.tight_layout()
  plt.savefig(f'./gaze_velocity/{str(index)}_hist.jpg', dpi=300)

  # Save or show the first figure
  plt.show()

"""For all subjects"""

base_dir = "./eye_tracking_user_study/gaze_positions"

min_list = []
max_list = []
mean_list = []

for index in range(1,41):
  exported_gaze_file = os.path.join(base_dir, f"{index}_gaze_positions.csv")
  exported_gaze = pd.read_csv(exported_gaze_file) #.dropna()
  # exported_gaze.info(verbose=True)

  exported_gaze.gaze_point_3d_z
  negative_z_mask = exported_gaze.gaze_point_3d_z < 0
  negative_z_values = exported_gaze.loc[negative_z_mask,["gaze_point_3d_z"]]
  exported_gaze.loc[negative_z_mask, ["gaze_point_3d_z"]] = negative_z_values * -1

  r, theta, psi = cart_to_spherical(exported_gaze, apply_rad2deg=True)
  # print(r)

  # plt.figure(figsize=(16, 4))

  # plt.subplot(1, 2, 1)
  # sphere_pos_over_time(
  #     exported_gaze.gaze_timestamp,
  #     data={"theta": theta, "psi": psi},
  #     unit="degrees"
  # )

  # plt.subplot(1, 2, 2)
  # sphere_pos(r, theta, psi, unit="degrees")

  # plt.tight_layout()

  squared_theta_diff = np.diff(theta) ** 2
  squared_psi_diff = np.diff(psi) ** 2
  deg_diff = np.sqrt(squared_theta_diff + squared_psi_diff)
  ts_diff = np.diff(exported_gaze.gaze_timestamp)
  deg_per_sec = deg_diff / ts_diff

  print(deg_per_sec.shape)
  min_list.append(min(deg_per_sec))
  max_list.append(max(deg_per_sec))
  mean_list.append(np.mean(deg_per_sec))

  time = exported_gaze.gaze_timestamp[:-1] - exported_gaze.gaze_timestamp.iloc[0]

  plt.figure(figsize=(16, 4))

  plt.subplot(1, 2, 1)
  sphere_pos_over_time(time, {"gaze velocity": deg_per_sec}, unit="deg/sec")
  plt.title("Gaze velocity over time")

  plt.subplot(1, 2, 2)
  plt.hist(deg_per_sec, bins=np.logspace(-1, np.log10(4000), 50))
  plt.title("Gaze velocity histogram")
  plt.xlabel("Gaze velocity [deg/sec]")

"""Pupil Coordinates"""

index = "10"

exported_pupil_csv = os.path.join("./", f'{str(index)}_pupil_positions.csv')
pupil_pd_frame = pd.read_csv(exported_pupil_csv)
print("Columns present in pupil data:")
list(pupil_pd_frame.columns)

pupil_pd_frame.head(10)

from IPython.display import display

# filter for 3d data
detector_3d_data = pupil_pd_frame[pupil_pd_frame.method == '2d c++']

# skip first 5 seconds to allow for the 3D model to converge
start_time = detector_3d_data.pupil_timestamp.iloc[0] + 5
detector_3d_data = detector_3d_data[detector_3d_data.pupil_timestamp > start_time]

# split in left/right eye
eye0_df = detector_3d_data[detector_3d_data.eye_id == 0]
eye1_df = detector_3d_data[detector_3d_data.eye_id == 1]
pd.options.display.float_format = '{:.3f}'.format

print("eye0 (right eye) data:")
display(eye0_df[['pupil_timestamp', 'eye_id', 'confidence', 'norm_pos_x', 'norm_pos_y', 'diameter_3d']].head(10))

print("eye1 data (left eye) data:")
display(eye1_df[['pupil_timestamp', 'eye_id', 'confidence', 'norm_pos_x', 'norm_pos_y', 'diameter_3d']].head(10))

eye0_high_conf_df = eye0_df[eye0_df['confidence'] > 0.6]
eye1_high_conf_df = eye1_df[eye1_df['confidence'] > 0.6]

plt.figure(figsize=(16, 5))
plt.plot(eye0_high_conf_df['pupil_timestamp'], eye0_high_conf_df['diameter_3d'])
plt.plot(eye1_high_conf_df['pupil_timestamp'], eye1_high_conf_df['diameter_3d'])
plt.legend(['eye0', 'eye1'])
plt.xlabel('Timestamps [s]')
plt.ylabel('Diameter [px]')
plt.title('Pupil Diameter (only high confidence values)')

# !mkdir /content/pupil_temporal

# plt.figure(figsize=(16, 5))

# plot left eye
plt.subplots(figsize=(8, 6))
plt.plot(eye1_high_conf_df['pupil_timestamp'], eye1_high_conf_df['norm_pos_x'])
plt.plot(eye1_high_conf_df['pupil_timestamp'], eye1_high_conf_df['norm_pos_y'])
plt.xlabel('Timestamps', fontsize=18)
plt.ylabel('norm_pos', fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.ylim([0, 1])
# plt.title('eye1')
plt.legend("xy", fontsize=14)
plt.tight_layout()
plt.savefig(f'./pupil_temporal/{index}_1.jpg', dpi=300)
plt.show()

# plot right eye
plt.subplots(figsize=(8, 6))
plt.plot(eye0_high_conf_df['pupil_timestamp'], eye0_high_conf_df['norm_pos_x'])
plt.plot(eye0_high_conf_df['pupil_timestamp'], eye0_high_conf_df['norm_pos_y'])
plt.xlabel('Timestamps', fontsize=18)
plt.ylabel('norm_pos', fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.ylim([0, 1])
# plt.title('eye0')
plt.legend("xy", fontsize=14)
plt.tight_layout()
plt.savefig(f'./pupil_temporal/{index}_0.jpg', dpi=300)
plt.show()

# !mkdir /content/pupil_spatial

# plt.figure(figsize=(16, 5))

# plot left eye
plt.subplots(figsize=(8, 6))
plt.scatter(eye1_high_conf_df['norm_pos_x'], eye1_high_conf_df['norm_pos_y'], c=eye1_high_conf_df['pupil_timestamp'])
plt.colorbar().ax.set_ylabel('Timestamps', fontsize=14)
plt.xlabel('norm_pos_x', fontsize=18)
plt.ylabel('norm_pos_y', fontsize=18)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.xlim([0, 1])
plt.ylim([0, 1])
# plt.title('eye1')
plt.tight_layout()
plt.savefig(f'./pupil_spatial/{index}_1.jpg', dpi=300)
plt.show()

# plot right eye
plt.subplots(figsize=(8, 6))
plt.scatter(eye0_high_conf_df['norm_pos_x'], eye0_high_conf_df['norm_pos_y'], c=eye0_high_conf_df['pupil_timestamp'])
plt.colorbar().ax.set_ylabel('Timestamps', fontsize=14)
plt.xlabel('norm_pos_x', fontsize=18)
plt.ylabel('norm_pos_y', fontsize=18)
plt.xlim([0, 1])
plt.ylim([0, 1])
# plt.title('eye0')
plt.tight_layout()
plt.savefig(f'./pupil_spatial/{index}_0.jpg', dpi=300)
plt.show()

