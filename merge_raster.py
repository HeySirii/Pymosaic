import rasterio
from rasterio.merge import merge
import glob
import os
# File and folder paths
dirpath = r"D:\2019.9.7SHB\19.9.8SHB_pm\WS\Oblique_25\CCws\ob_25\Productions\Ortho"
out_fp = r"D:\2019.9.7SHB\19.9.8SHB_pm\WS\Oblique_25\CCws\ob_25\Productions\Ortho\mosaic.tif"
# Make a search criteria to select the Tif files
search_criteria = "*.tif"
q = os.path.join(dirpath, search_criteria)
tif_fps = glob.glob(q)
src_files_to_mosaic = []
for fp in tif_fps:
     src = rasterio.open(fp)
     src_files_to_mosaic.append(src)
src_files_to_mosaic
# Merge function returns a single mosaic array and the transformation info
mosaic, out_trans = merge(src_files_to_mosaic)

# Copy the metadata
out_meta = src.meta.copy()

# Update the metadata
out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans,
                      "crs": "+proj=utm +zone=50 +ellps=WGS84 +units=m +no_defs "
 }
)
# Write the mosaic raster to disk
with rasterio.open(out_fp, "w", **out_meta) as dest:
      dest.write(mosaic)