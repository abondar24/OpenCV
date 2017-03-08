#include "histogram1d.h"

Histogram1D::Histogram1D(){
    histSize[0] = 256;
    hranges[0] = 0.0;
    hranges[1] = 255.0;
    ranges[0] = hranges;
    channels[0] = 0;

}

cv::MatND Histogram1D::getHistogram(const cv::Mat &image){
    cv::MatND hist;

    cv::calcHist(&image,1,channels,cv::Mat(),hist,1,histSize,ranges);

    return hist;
}


cv::Mat Histogram1D::getHistogramImage(const cv::Mat &image){
    cv::MatND hist = getHistogram(image);

    double maxVal = 0;
    double minVal = 0;

    cv::minMaxLoc(hist, &minVal,&maxVal,0,0);

    cv::Mat histImg(histSize[0], histSize[0], CV_8U, cv::Scalar(255));

    // set higest point at 90% of nbins
    int hpt = static_cast<int>(0.9*histSize[0]);

    // draw a vertical line for each bin
    for (int h = 0; h<histSize[0];h++){
        float binVal = hist.at<float>(h);
        int intensity = static_cast<int>(binVal*hpt/maxVal);

        cv::line(histImg, cv::Point(h,histSize[0]),
                cv::Point(h,histSize[0]-intensity),
                cv::Scalar::all(0));
    }

    return histImg;
}

cv::Mat Histogram1D::applyLookUp(const cv::Mat& image, const cv::Mat& lookup){
    cv::Mat res(image.rows,image.cols,CV_8U);

    cv::LUT(image,lookup,res);
    return res;
}

cv::Mat Histogram1D::produceLookUpTable(){
    int dim(256);
    cv::Mat lut(1,&dim,CV_8U);

    for (int i=0;i<256;i++){
        lut.at<uchar>(i) = 255-i;
    }

    return lut;
}

// improve image contrast
cv::Mat Histogram1D::stretch(const cv::Mat &image, int minValue){
    cv::MatND hist = getHistogram(image);

    // find left extrimity of hist
    int imin=0;
    for (;imin<histSize[0];imin++){
        std::cout<<hist.at<float>(imin)<<std::endl;
        if (hist.at<float>(imin) > minValue){
            break;
        }

    }

    // find right extrimity
    int imax=histSize[0]-1;
    for (;imax>=0;imax--){
        if (hist.at<float>(imax)>minValue){
            break;
        }
    }

    int dim(256);
    cv::Mat lut(1,&dim,CV_8U);

    for (int i=0;i<256;i++){
        if (i<imin) {
            lut.at<uchar>(i)=0;
        } else if (i>imax) {
            lut.at<uchar>(i)=255;
        } else {
            lut.at<uchar>(i)=static_cast<uchar>(
                        255.0*(i-imin)/(imax-imin)+0.5);
        }
    }

    cv::Mat result;
    result = applyLookUp(image,lut);
    return result;

}


