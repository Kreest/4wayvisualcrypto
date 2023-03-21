Encode multiple images in two visual cryptography shares.

Algorithm from "Research on Rotation Visual Cryptography Scheme" by Zhengxin Fu; Bin Yu.

Base code inspired by https://gist.github.com/deibit/ccc2b55ae9eab94392e4118c05aded52

NOTE: This 3AM terribly written code, but it works.

Example usage:
`python multi.py test.png eat.png sea.png weed.png`

There will be two output files, `test_A.png` and `test_B.png`. 
You'll need to convert white to transparent on the image you wish to overlay.

Make sure the images are the same dimension

MIT License
