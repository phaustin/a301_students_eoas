import a301_lib
import sat_lib.hdftools.h5dump as h5dump

stars = '*'*50
print(f"\n\n{stars}\n\n")
filename = (a301_lib.sat_data / 'h5_dir').glob("ch30*2105*h5")
filename = list(filename)[0]
filename = str(filename.resolve())
print(f"here is the ch30 file: {filename}")
h5dump.main(filename)
print(f"\n\n{stars}\n\n")
filename = (a301_lib.sat_data / 'h5_dir').glob("geom*2105*h5")
filename = list(filename)[0]
filename = str(filename.resolve())
print(f"here is the geom file: {filename}")
h5dump.main(filename)
print(f"\n\n{stars}\n\n")

