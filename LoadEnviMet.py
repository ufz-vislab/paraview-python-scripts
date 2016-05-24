# Run this script in the Python shell and then call"
# LoadEnviMet('X:\\caro\\Vis_Bayr-Bahnhof\\EnviMet\\ostwind', 'istzustand',  'neuebebauung')

# ['%zkart', 'ClassedLADandShelters', 'Flowu-m/s', 'Flowv-m/s', 'Floww-m/s', 'WindSpeed-m/s', 'WindSpeedChange-%', 'WindDirection-deg', 'PressurePerturbation-Diff', 'Pot.Temperature-K', 'Pot.Temperature-DiffK', 'Pot.TemperatureChange-K/h', 'Spec.Humidity-g/kg', 'RelativeHumidity-%', 'TKE-m/m', 'Dissipation-m/m', 'VerticalExchangeCoef.Impuls-m/s', 'HorizontalExchangeCoef.Impuls-m/s', 'AbsoluteLAD-m/m', 'DirectSwRadiation-W/m', 'DiffuseSwRadiation-W/m', 'ReflectedSwRadiation-W/m', 'LwRadiationEnvironment-W/m', 'Sky-View-FactorBuildings', 'Sky-View-FactorBuildings+Vegetation', 'TemperatureFlux-K*m/s', 'VapourFlux-g/kg*m/s', 'WateronLeafes-g/m', 'WallTemponCellborderx-K', 'WallTemponCellbordery-K', 'WallTemponCellborderz-K', 'LeafTemperature-K', 'LocalMixingLength-m', 'PMVValue', 'PPDValue', 'MeanRadiantTemperature-K', 'PM10Concentration-g/m', 'PM10Source-g/s', 'DepositionVelocity-mm/s', 'TotalDeposedPM10-g/m', 'DeposedPM10Timeaveraged-g/m*s', 'TKEnormalised1D', 'Dissipationnormalised1D', 'Kmnormalised1D', 'TKEMechanicalTurbulenceProd.', 'StomataResistance-m/s', 'CO2-mg/m3', 'CO2-ppm', 'PlantCO2Flux-mg/kg*m/s', 'DivRlwTempchange-K/h', 'LocalmassbudgetPM10-g/s*m']

# ['zTopo-m', 'TSurface-K', 'TSurfaceDiff.-K', 'TSurfaceChange-K/h', 'qSurface-g/kg', 'uvaboveSurface-m/s', 'Sensibleheatflux-W/m', 'ExchangeCoeff.Heat-m/s', 'Latentheatflux-W/m', 'SoilheatFlux-W/m', 'SwDirectRadiation-W/m', 'SwDiffuseRadiation-W/m', 'LambertFactor', 'LongwaveRadiationBudget-W/m', 'LongwaveRad.fromvegetation-W/m', 'LongwaveRad.fromenvironment-W/m', 'WaterFlux-g/-ms', 'Sky-View-Faktor', 'BuildingHeight-m', 'SurfaceAlbedo', 'DepositionSpeed-mm/s', 'MassDeposed-g/m']
import re, os
#os.chdir('X:\\caro\\Vis_Bayr-Bahnhof\\EnviMet\\ostwind\\istzustand')

def LoadEnviMet(path, dir1, dir2):
    dir = path + os.sep + dir1 + os.sep
    array_status = ['Pot.Temperature-K','Flowu-m/s', 'Flowv-m/s', 'Floww-m/s', 'WindSpeed-m/s']
    array_status_fx = ['TSurface-K', 'Sensibleheatflux-W/m', 'Latentheatflux-W/m', 'SoilheatFlux-W/m']

    all_files = os.listdir(dir)
    files = []
    files_neu = []
    files_fx = []
    files_fx_neu = []
    for file in sorted(all_files):
        if file.endswith('.EDI') and '_AT_' in file:
            files.append(dir + file)
            files_neu.append(dir.replace(dir1, dir2) + file.replace('Bhf.1', 'Bhf.1W'))
        if file.endswith('.EDI') and '_FX_' in file:
            files_fx.append(dir + file)
            files_fx_neu.append(dir.replace(dir1, dir2) + file.replace('Bhf.1', 'Bhf.1W'))

    at = [files, files_neu]
    for f in at:
        reader = ENVImetReader(FileName = f)
    # Instead of a simple reader = ENVImetReader(FileName = files)
    # the following also sets the pipeline objects name
    # COMMENT: does not initalize time steps ...
    #reader = servermanager.sources.ENVImetReader(FileName = files)
    #servermanager.Register(reader, registrationName="ostwind-ist")
        reader.PointArrayStatus = array_status
        reader.UpdatePipeline()

    #reader_neu = ENVImetReader(FileName = files_neu)
    #reader_neu = servermanager.sources.ENVImetReader(FileName = files_neu)
    #servermanager.Register(reader_neu, registrationName="ostwind-bebauung")
    #reader_neu.PointArrayStatus = array_status
    #reader_neu.UpdatePipeline()

    fx = [files_fx, files_fx_neu]
    for f in fx:
        reader = ENVImetReader(FileName = f)
        reader.PointArrayStatus = array_status_fx
        reader.UpdatePipeline()

#dp =  GetDisplayProperties(reader)
#dp.Representation = 'Surface'
#dp.LookupTable = MakeBlueToRedLT(0, 0.5)
#dp.ColorArrayName = '%zkart'
#Render()
