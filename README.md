### DESCRIPTION ###
This project aims to compare two deep learning techniques in the task of learning musical styles and generating novel musical content. Long Short Term Memory (LSTMs), a supervised learning algorithm is used, which is a variation of the Recurrent Neural Network (RNN), frequently used for sequential data. Another technique explored is Generative Adversarial Networks (GANs), an unsupervised approach which is used to learn a distribution of a particular style, and novelly combine components to create sequences. The representation of data from the MIDI files as chord and note embedding are essential to the performance of the models. This type of embedding in the network help it to discover structural patterns in the samples. Through the study, it is seen how a supervised learning technique performs better than the unsupervised one. A study helped in obtaining a Mean Opinion Score (MOS), which was used as an indicator of the comparative quality and performance of the respective techniques.


The models generated music of specified lengths and BPM (Beats per minute). Ample number of samples were created so as to increase the sample size of comparison. Further, a small study was conducted to get a better metric. Subjects in the study were made to listen to samples of both the models and a few human samples from the real world in a random order. The Mean Opinion Score (MOS) indicator was used as the metric. The listeners in the study were also asked to classify the sample as human or AI generated. The study involved around 150 participants from diverse backgrounds. Some, with fairly good understanding of music theory, some who don’t necessarily understand music theory, but listen to a lot of music regularly and finally, some, who don’t listen to music regularly. The MOS for both the models combined was 3.55. Individually, the LSTM model performed better with a MOS of 3.80 compared to the GAN model which had a MOS of 3.17. The MOS for each of the music samples is shown in Fig below. It was also observed that 63.8% of the participants classified the samples of the LSTM model as human composed as shown in Fig below. This implies that the participants identified in these samples, some semblance to the human ones in terms of structural patterns, emotion or just melody. 


![screenshot](https://github.com/vcsheel/MusicGeneration/blob/master/image4.png)

![screenshot](https://github.com/vcsheel/MusicGeneration/blob/master/Screen%20Shot%202019-05-10%20at%2012.14.19%20AM.png)

### BACKEND SERVER  ###
1. Download and place the weights file in the /server folder
    https://drive.google.com/open?id=1gl9icPYtfDMPS-H2xnwwBrSnCsJnzCCT

2. start the backend server : 
    ==> cd to /server
    ==> npm start

### FRONT END ###

======> Start with : 
                    ng serve --port 4000 --live-reload false

