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
