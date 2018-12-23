#include "kalman_filter.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;

/* 
 * Please note that the Eigen library does not initialize 
 *   VectorXd or MatrixXd objects with zeros upon creation.
 */

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
}

void KalmanFilter::Predict() {
  /**
   * TODO: predict the state
   */
  
  x_ = F_ * x_;
  MatrixXd Ft = F_.transpose();
  P_ = F_ * P_ * Ft + Q_;
  
}
// steps common for KalmanFilter and Extended KF
void KalmanFilter::UpdateCommon(const VectorXd &y) {
  MatrixXd Ht = H_.transpose();
    MatrixXd S = H_ * P_ * Ht + R_;
    MatrixXd S_inv = S.inverse();
    MatrixXd K = P_ * Ht * S_inv;
    x_ = x_ + (K * y);
    int size = x_.size();
    MatrixXd I = MatrixXd::Identity(size, size);
    P_ = (I * K * H_) * P_;
}

void KalmanFilter::Update(const VectorXd &z) {
  /**
   * TODO: update the state by using Kalman Filter equations
   */
  
  VectorXd y = z - H_ * x_;
  UpdateCommon(y);
  
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  /**
   * TODO: update the state by using Extended Kalman Filter equations
   */
  double px = x_(0);
  double py = x_(1);
    double vx = x_(2);
    double vy = x_(3);
    // approximate corresponding rho, phi, rhodot
    double rho = sqrt(px * px + py * py);
    double phi = atan(py / px);
    double rhodot = (px * vx + py * vy) / rho;
  
    VectorXd h = VectorXd(3);
    h << rho, phi, rhodot;
  
    VectorXd y = z - h;
    // continue to do kalman filter
    UpdateCommon(y);
  
}
