# Hypothesis Testing Scenarios

Applying statistical hypothesis testing to real-world scenarios using paired and one-sample t-tests.

## P1: Football Speed Improvement Analysis

### Objective:

Determine if a speed and agility camp improved football players’ 40-yard dash times.

### Methodology:

- Test: Paired t-test (before vs. after measurements)
- Null Hypothesis (H₀): Mean difference in times before and after the camp is 0
- Alternate Hypothesis (H₁): Mean difference in times before and after the camp > 0

Data: 15 players’ 40-yard dash times before and after the camp

### Results:

- Mean difference = 1.83 seconds
- t-value = 4.387, df = 14
- p-value = 0.00031

### Conclusion:
- Since t-value > critical t and p < 0.05, we reject H₀.

***Insight: The camp significantly improved players’ speed.***

## P2: Harvard LSAT Score Analysis

### Objective:
Test whether incoming Harvard Law School freshmen have LSAT scores higher than the general mean of 521.

### Methodology:

- Test: One-sample t-test
- Null Hypothesis (H₀): Mean LSAT = 521
- Alternate Hypothesis (H₁): Mean LSAT > 521

Data: 25 Harvard freshmen, mean = 589, SD = 37

### Results:

- t-value = 9.189, df = 24
- Critical t = 1.711, α = 0.05

### Conclusion:
- Since t-value > critical t, we reject H₀.

***Insight: Harvard freshmen scored significantly higher than the average law student LSAT score.***
