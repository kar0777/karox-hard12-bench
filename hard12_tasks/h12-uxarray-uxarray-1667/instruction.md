You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Filter non-spatial variables from UGRID datasets


### Discussed in https://github.com/UXARRAY/uxarray/discussions/1324

<div type='discussions-op-text'>

<sup>Originally posted by **Chrismarsh** July 24, 2025</sup>
What is the approach to save a subset ugrid to disk? For example, suppose I do

```
# massive dataset
ds = ux.open_mfdataset('output.2017.partial/output.2017.nc',
                       'output.2017.partial/output.2017.nc', 
                       parallel=False, lock=False)

# subset part of it
elev = ds.Elevation.subset.bounding_box(lon, lat)

# save subset
elev.to_xarray().to_netcdf('test2.nc', engine="netcdf4")
```

The test2.nc file does not contain valid ugrid topology:

```
$ ncdump -h test2.nc
netcdf test2 {
dimensions:
        n_face = 142546 ;
variables:
        double Mesh2_face_x(n_face) ;
                Mesh2_face_x:_FillValue = NaN ;
                Mesh2_face_x:standard_name = "latitude" ;
                Mesh2_face_x:long_name = "Characteristics latitude of 2D mesh triangle (e.g. circumcenter coordinate)." ;
                Mesh2_face_x:units = "degrees_north" ;
        double Mesh2_face_y(n_face) ;
                Mesh2_face_y:_FillValue = NaN ;
                Mesh2_face_y:standard_name = "latitude" ;
                Mesh2_face_y:long_name = "Characteristics latitude of 2D mesh triangle (e.g. circumcenter coordinate)." ;
                Mesh2_face_y:units = "degrees_north" ;
        double face_lon(n_face) ;
                face_lon:_FillValue = NaN ;
                face_lon:standard_name = "latitude" ;
                face_lon:long_name = "Characteristics latitude of 2D mesh triangle (e.g. circumcenter coordinate)." ;
                face_lon:units = "degrees_north" ;
        double face_lat(n_face) ;
                face_lat:_FillValue = NaN ;
                face_lat:standard_name = "latitude" ;
                face_lat:long_name = "Characteristics latitude of 2D mesh triangle (e.g. circumcenter coordinate)." ;
                face_lat:units = "degrees_north" ;
        double Elevation(n_face) ;
                Elevation:_FillValue = NaN ;
                Elevation:_QuantizeBitGroomNumberOfSignificantDigits = 4 ;
                Elevation:mesh = "Mesh2" ;
                Elevation:location = "face" ;
                Elevation:coordinates = "Mesh2_face_x Mesh2_face_y face_lat face_lon" ;
}

```</div>

