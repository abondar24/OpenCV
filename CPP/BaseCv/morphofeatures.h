#ifndef MORPHOFEATURES_H
#define MORPHOFEATURES_H
#include <opencv2/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class MorphoFeatures
{
public:

    MorphoFeatures(): threshold(-1),
        cross(5,5,CV_8U,cv::Scalar(0)),
        diamond(5,5, CV_8U,cv::Scalar(1)),
        square(5,5,CV_8U,cv::Scalar(1)),
        x(5,5,CV_8U,cv::Scalar(0)){

        //cross-shaped structuring element
        for (int i=0; i<5; i++){
            cross.at<uchar>(2,i) = 1;
            cross.at<uchar>(i,2) = 1;
        }

        //diamond-shaped structuring element
        diamond.at<uchar>(0,0) = 0;
        diamond.at<uchar>(0,1) = 0;
        diamond.at<uchar>(1,0) = 0;
        diamond.at<uchar>(4,4) = 0;
        diamond.at<uchar>(3,4) = 0;
        diamond.at<uchar>(4,3) = 0;
        diamond.at<uchar>(4,0) = 0;
        diamond.at<uchar>(4,1) = 0;
        diamond.at<uchar>(3,0) = 0;
        diamond.at<uchar>(0,4) = 0;
        diamond.at<uchar>(0,3) = 0;
        diamond.at<uchar>(1,4) = 0;

        for (int i=0; i<5; i++){
            x.at<uchar>(i,i) = 1;
            x.at<uchar>(4-i,i) = 1;
        }
    }

    cv::Mat getEdges( const cv::Mat &image);
    void applyThreshold(cv::Mat& result);
    void setThreshold(int t);
    int getThreshold() const;
    cv::Mat getCorners(const cv::Mat &image);
    void drawOnImage(const cv::Mat& binary, cv::Mat& image);

private:
    int threshold;
    cv::Mat cross;
    cv::Mat diamond;
    cv::Mat square;
    cv::Mat x;
};

#endif // MORPHOFEATURES_H
