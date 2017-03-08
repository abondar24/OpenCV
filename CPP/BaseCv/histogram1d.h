#ifndef HISTOGRAM1D_H
#define HISTOGRAM1D_H
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

class Histogram1D
{
public:
    Histogram1D();
    cv::Mat getHistogramImage(const cv::Mat &image);
    cv::Mat applyLookUp(const cv::Mat& image, const cv::Mat& lookup);
    cv::Mat produceLookUpTable();
    cv::Mat stretch(const cv::Mat &image, int minValue=0);

private:
    int histSize[1]; //number of bins
    float hranges[2]; // min and max pixel val
    const float* ranges[1];
    int channels[1];

    cv::MatND getHistogram(const cv::Mat &image);
};

#endif // HISTOGRAM1D_H
