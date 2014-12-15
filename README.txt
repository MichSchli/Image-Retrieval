README

	This program contains an implementation of a content-based image retrieval system relying on precomputed SIFT
	keys and kmeans clustering. It is written using the Anaconda distribution of Python 2.7, and relies on the 
	libraries scikit-learn for clustering, pickle for serialization, and scikit-image for displaying images.
	
	SIFT-files should follow the standard format used by VLFeat, and placed directly next to the corresponding
	images.
	
INSTRUCTIONS	

	The program should be accessed through the main file ImageRetriever.py, either from the command line with "python
	ImageRetriever.py", or imported as a module.
	
	If run in the command line, a small text interface is provided. Here, the user is allowed to select between precomputed
	indexings and computing a new indexing. Moreover, the user is allowed to select an image and find a match. Note that
	all images must be accompanied by a precomputed .sift-file with the same name.

	If imported as a module, the functionality should be accessed through the function show_best_match.
	
	The library files Codebook.py and ImageLibraryLoader.py contain various testing functions, which can be accessed
	by running them from the command line.

	Be aware that indexing and especially codebook generation are expensive operations computationally. As such, we recommend
	using a stored indexing. We have not included such a file, nor have we included the images or sift keys for the
	Caltech 101 dataset. This is due mainly to the size constraints on the Absalon system. Should you wish to use 
	either, please contact us and we shall provide an archive.

CONTACT
	
	If there is any problem, please contact me (Michael Schlichtkrull) through my student mail qwt774@alumni.ku.dk.
