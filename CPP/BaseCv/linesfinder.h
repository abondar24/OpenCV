#ifndef LINESFINDER_H
#define LINESFINDER_H
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class LinesFinder
{
public:
    LinesFinder(): deltaRho(1), deltaTheta(3.14/180),
                   minVote(10), minLength(0.), maxGap(0.) {}

    void setAccResolution(double dRho, double dTheta);

    void setMinVote(int minV);

    void setLineLengthAndGap(double length, double gap);

    std::vector<cv::Vec4i> findLines(cv::Mat& binary);

    void drawDetectedLines(cv::Mat &image,
                               cv::Scalar color=cv::Scalar(128,128,128));

private:
    cv::Mat img;
    std::vector<cv::Vec4i> lines;

    // accumulator res parameters
    double deltaRho;
    double deltaTheta;

    // min number of votes that a line
    // must recieve before being considered
    int minVote;

    // min length for a line
    double minLength;

    // max allowed gap along the line
    double maxGap;


};

#endif // LINESFINDER_H
