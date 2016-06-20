## Running python scripts with ParaView

Python scripts are run through ```pvpython``` binary of ParaView (usually found in ./bin dir of PV).

Run a script, for example by the command
```./ParaView-5.0.0-Qt4-OpenGL2-MPI-Linux-64bit/bin/pvpython scripts/CompareTwoTimesteps.py MyFirst.vtu MySecond.vtu```

You can also combine this with handy bash scripting (loops, conditionals etc):
```for i in $(cat MyVTUList.txt); do ./ParaView-5.0.0-Qt4-OpenGL2-MPI-Linux-64bit/bin/pvpython scripts/CompareTwoTimesteps.py ${i}; done```

### Caveats
Make sure to use at least ParaView version 5.0 (previous version seem to have a bug with script arguments). 
Also, you probably need to give the full path of pvpython (symbolic links didn't work), as pvpython expects some libraries relative to the binary (strange...).


## ParaView python scripts for EnviMet visualizations

### Create XML Plugin from Python file

```bash
python python_filter_generator.py ArrayDiffFilter.py plugins/ArrayDiffFilter.xml
```

## Usage

### Load XML plugin

In * Menu / Tools / Plugin Manager* load the xml-file. Make sure to switch file type to `.xml`.

### Load EnviMet time series

- Run the script `LoadEnviMet.py` in the Python shell
- Call e.g. `LoadEnviMet('X:\\caro\\Vis_Bayr-Bahnhof\\EnviMet\\ostwind', 'istzustand',  'neuebebauung')``
