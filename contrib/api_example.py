from lap_tracker.detection import PeakDetector
from lap_tracker.tracker import Tracker
from lap_tracker.io import TiffFile

fname = 'my_awesome_ome_file.tif'
tf = TiffFile(fname)

peaks_detector = PeakDetector(tf or fname)
peaks_detector.run(paralell=True)

tracker = Tracker(peaks_detector.peaks)
tracker.run()

tracker.show()

print(tracker.traj)
