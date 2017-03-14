#include "linesfinder.h"

#include <opencv2/highgui.hpp>

void LinesFinder::setAccResolution(double dRho, double dTheta){
    deltaRho = dRho;
    deltaTheta = dTheta;
}

void LinesFinder::setMinVote(int minV){
    minVote = minV;
}

void LinesFinder::setLineLengthAndGap(double length, double gap){
    minLength = length;
    maxGap = gap;
}

std::vector<cv::Vec4i> LinesFinder::findLines(cv::Mat& binary){
    lines.clear();
    cv::HoughLinesP(binary,lines,
                     deltaRho,deltaTheta,minVote,
                     minLength,maxGap);

    return lines;
}

void LinesFinder::drawDetectedLines(cv::Mat &image, cv::Scalar color){

    // draw lines
    std::vector<cv::Vec4i>::const_iterator it2 = lines.begin();

    while (it2!=lines.end()){
        cv::Point pt1((*it2)[0],(*it2)[1]);
        cv::Point pt2((*it2)[2],(*it2)[3]);

        cv::line(image, pt1, pt2,color);

        ++it2;
    }


}
