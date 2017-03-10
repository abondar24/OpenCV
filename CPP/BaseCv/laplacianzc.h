#ifndef LAPLACIANZC_H
#define LAPLACIANZC_H
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class LaplacianZC
{
public:
    LaplacianZC():aperture(3){}

    void setAperture(int a);
    cv::Mat computeLaplacian(const cv::Mat& image);
    cv::Mat getLaplacianImage(double scale=-1.0);
    cv::Mat getZeroCrossings(float threshold=1.0);


private:
   cv::Mat img;

   // 32-bit float image of the laplacian kernel
   cv::Mat laplace;

   //aperture size of the laplacian kernel
   int aperture;

};

#endif // LAPLACIANZC_H
