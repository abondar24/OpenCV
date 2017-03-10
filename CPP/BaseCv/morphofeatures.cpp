#include "morphofeatures.h"


cv::Mat MorphoFeatures::getEdges( const cv::Mat &image){
    cv::Mat result;

    cv::morphologyEx(image,result, cv::MORPH_GRADIENT, cv::Mat());
    applyThreshold(result);

    return result;

}

void MorphoFeatures::applyThreshold(cv::Mat& result){
    if (threshold>0){
        cv::threshold(result, result, threshold, 255, cv::THRESH_BINARY);
    }
}


void MorphoFeatures::setThreshold(int t) {

    threshold= t;
}

int MorphoFeatures::getThreshold() const {

    return threshold;
}

cv::Mat MorphoFeatures::getCorners(const cv::Mat &image){
    cv::Mat result;

    cv::dilate(image,result,cross);
    cv::erode(result,result,diamond);

    cv::Mat result2;

    cv::dilate(image,result2,x);
    cv::erode(result2,result2,square);

    //conrners are obtained by diffrerencing two closed images
    cv::absdiff(result2, result,result);
    applyThreshold(result);

    return result;
}


void MorphoFeatures::drawOnImage(const cv::Mat& binary, cv::Mat& image){
    cv::Mat_<uchar>::const_iterator it = binary.begin<uchar>();
    cv::Mat_<uchar>::const_iterator itend = binary.end<uchar>();

    for (int i=0;it!=itend;++it,++i){
        if (!*it){
            cv::circle(image, cv::Point(i%image.step,i/image.step),5,cv::Scalar(255,0,0));
        }
    }
}
