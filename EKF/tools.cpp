#include "tools.h"
#include <iostream>

using Eigen::VectorXd;
using Eigen::MatrixXd;
using std::vector;

Tools::Tools() {}

Tools::~Tools() {}

VectorXd Tools::CalculateRMSE(const vector<VectorXd> &estimations,
                              const vector<VectorXd> &ground_truth) {
  /**
   * TODO: Calculate the RMSE here.
   */
  
  // initialize rmse
  VectorXd rmse(4);
  rmse << 0, 0, 0, 0;
  unsigned int total_num_estimations = estimations.size();
  // check input
  if (total_num_estimations == 0) {
    std::cout << "Error: No input" << std::endl;
    return rmse;
  }
  // check if they have the same size
  if (total_num_estimations != ground_truth.size()) {
    std::cout << "Error: Invalid input." << std::endl;
    return rmse;
  }
  
  // sum residuals
  for (unsigned int i = 0; i < total_num_estimations; ++i) {
    VectorXd residuals = estimations[i] - ground_truth[i];
    residuals = residuals.array() * residuals.array();
    rmse += residuals;
  }
  // average
  rmse /= total_num_estimations;

  // mean squared root
  rmse = rmse.array().sqrt();

  return rmse;
}

MatrixXd Tools::CalculateJacobian(const VectorXd& x_state) {
  /**
   * TODO:
   * Calculate a Jacobian here.
   */
  // retrieve coordinates
  double px = x_state(0);
  double py = x_state(1);
  double vx = x_state(2);
  double vy = x_state(3);
  
  MatrixXd Hj(3, 4);
  // preparation to calculate the matrix
  double c1 = px * px + py * py;
  if (std::abs(c1) < 0.0000001) {
  c1 = 0.0000001;
  }
  double c2 = sqrt(c1);
  double c3 = c1 * c2;
  
  // calculate jacobian matrix
  Hj << (px / c2), (py / c2), 0, 0,
    -(py / c1), (px / c1), 0, 0,
    (py * (vx*py - vy*px)) / c3, (px * (vy*px - vx*py))/ c3, px / c2, py / c2;
       
  return Hj;
}
