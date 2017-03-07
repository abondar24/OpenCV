#include "colordetecor.h"




cv::Mat ColorDetecor::process(const cv::Mat &image){
    result.create(image.rows,image.cols,CV_8U);

    cv::Mat_<cv::Vec3b>::const_iterator it= image.begin<cv::Vec3b>();
    cv::Mat_<cv::Vec3b>::const_iterator itend= image.end<cv::Vec3b>();
    cv::Mat_<uchar>::iterator itout= result.begin<uchar>();

    // for each pixel
    for ( ; it!= itend; ++it, ++itout) {

        if (getDistance(*it)<minDist) {

            *itout= 255;

        } else {

            *itout= 0;
        }

    }

    return result;
}

int ColorDetecor::getDistance(const cv::Vec3b& color) const{
    return abs(color[0]-target[0])+
            abs(color[1]-target[1])+
            abs(color[2]-target[2]);

}

void ColorDetecor::setColorDistanceThreshold(int distance){
    if (distance<0){
        distance=0;
    }

    minDist = distance;

}

int ColorDetecor::getColorDistanceThreshold(){
    return minDist;
}


void  ColorDetecor::setTargetColor(unsigned char red,
                    unsigned char green,
                    unsigned char blue){

    target[2] = red;
    target[1] = green;
    target[0] = blue;
}

void  ColorDetecor::setTargetColor(cv::Vec3b color){
    target = color;
}

cv::Vec3b  ColorDetecor::getTargetColor() const{
    return target;
}


