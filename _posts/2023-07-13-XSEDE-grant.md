---
layout: post
title: NCSA-XSEDE Grant Awarded for in silico Antibody Engineering Computational Research
date: 2023-07-13

---

  *Exciting Announcement! 🎉*

 
    We are thrilled to announce that we have been awarded a grant from the
    XSEDE- National Center for Supercomputing!
 

  <img src="/images/XSEDE1.png" alt="XSEDE Logo">

  
    This grant will enable me to use the powerful
    *RockFish Cluster* at John's Hopkins University for our research.
    The opportunity to harness the capabilities of this supercomputer is both an honor
    and a boon for the advancement of my work.
 
    
    We are thrilled to announce that our innovative project, "Unlocking Antibody-Antigen Interactions: An In Silico Approach to Optimize PD-L1 Immune Checkpoint Inhibitors", has been recognized and funded by NCSI-XSEDE. This pioneering computational biochemistry research focuses on the critical role of Complementarity-Determining Regions (CDRs) in antibody-antigen interactions, specifically targeting the complex interplay with Programmed death-ligand 1 (PD-L1), a key player in cancer immune evasion.

Our methodology marries cutting-edge machine learning and molecular dynamics simulations, providing a holistic and comprehensive approach to understand and optimize PD-L1 immune checkpoint inhibitors. We utilize the robust predictive capabilities of deep learning tools, like Rosetta and AlphaFold, to anticipate the 3D structures of antibody-PD-L1 complexes based on sequence data. This allows us to comprehend the structural impacts of modifications in CDRs with unprecedented precision.

Following structure prediction, we deploy Molecular Dynamics simulations to investigate the dynamics and stability of these intricate protein-protein complexes. The use of MMPBSA calculations, further, enables us to estimate the binding free energy (∆G) between the antibody and PD-L1, offering a quantitative measure of how changes in CDRs affect binding affinity.

A noteworthy aspect of our research is the efficient utilization of high-performance computing resources, particularly the deployment of GPUs on the Johns Hopkins RockFish Cluster. This allows us to effectively manage demanding calculations and handle extensive datasets, accelerating our research process and enhancing output accuracy.

By combining our expertise in Linux, Python, Molecular Dynamics (specifically with AMBER), MMPBSA, Rosetta, and other relevant bioinformatics databases, we are confident in pushing the boundaries of computational biochemistry and contributing significantly to advancements in cancer treatment. This project underpins our commitment to driving forward the frontiers of science using high-performance computing and innovative methodologies.
    
    Our project takes advantage of Support Vector Regression (SVR), a powerful machine learning technique used for both regression and classification problems, to create a hierarchical structure of ∆G binders derived from our MMPBSA experiments.

Starting with our MMPBSA calculations, we generate binding free energy estimates for a multitude of antibody-PD-L1 complexes. These estimates, however, only provide a raw numerical value for the binding affinity. To extract more insightful patterns and relationships from this data, we turn to SVR.

SVR is particularly suited for this task due to its ability to handle high-dimensional data and its robustness against overfitting, making it ideal for our data-rich computational biochemistry project. It allows us to map out complex, non-linear relationships between various parameters and the binding affinity, transforming raw MMPBSA results into a more meaningful structure.

Our SVR model takes as input the various parameters derived from the complex structures and MMPBSA calculations, including features related to the conformations, the physicochemical properties, and the dynamic behaviour of the complexes. The output of the model is a prediction of the binding free energy.

By doing this, we create a hierarchical structure that categorizes the antibody-PD-L1 complexes based on their predicted ∆G values. This gives us a more refined and detailed understanding of how changes in CDRs influence binding affinity, beyond what simple MMPBSA calculations can offer.

Training the SVR model involves a careful optimization process, where we tune the hyperparameters to achieve the best performance. We validate the model using a separate set of data, ensuring that our model is robust and reliable.

In this way, SVR serves as a crucial bridge in our research, connecting raw data from our simulations with more nuanced, predictive insights that can guide our understanding and optimization of PD-L1 immune checkpoint inhibitors.
    
    The objective of SVR is to find a function $$f(x)$$ that has at most $$\epsilon$$ deviation from the actual training responses $$y_i$$ for all the training data, and at the same time, is as flat as possible. This is achieved by minimizing the following cost function:

$$
C\sum_{i=1}^{n}L_{\epsilon}(y_i-f(x_i)) + \frac{1}{2}||w||^2
$$

where

$$
L_{\epsilon}(y_i-f(x_i)) = 
\begin{cases}
0, & |y_i-f(x_i)|\leq\epsilon \\
|y_i-f(x_i)|-\epsilon, & \text{otherwise}
\end{cases}
$$

Here, $$L_{\epsilon}(y_i-f(x_i))$$ is the $$\epsilon$$-insensitive loss function, $$w$$ is the vector of weights, and $$C$$ is a parameter that determines the trade-off between the flatness of $$f(x)$$ and the amount up to which deviations larger than $$\epsilon$$ are tolerated.

In its simplest linear form, $$f(x)$$ can be written as $$f(x)=wx+b$$, where $$w$$ and $$b$$ are the weights and bias that we need to find. However, in most cases, the relationship between $$x$$ and $$y$$ is non-linear, and we need to map the data to a high-dimensional feature space using a kernel function $$\phi(x)$$. The function $$f(x)$$ then becomes $$f(x)=w\phi(x)+b$$. In this case, the optimization problem can be solved more efficiently in the dual space using the kernel trick, which avoids explicitly calculating the mapping $$\phi(x)$$.

Commonly used kernel functions include the linear kernel ($$k(x, x') = x \cdot x'$$), the polynomial kernel ($$k(x, x') = (x \cdot x' + c)^d$$), and the Radial Basis Function (RBF) or Gaussian kernel ($$k(x, x') = \exp(-\gamma ||x - x'||^2)$$), with $$d$$, $$c$$, and $$\gamma$$ being hyperparameters that need to be tuned.


For further details or inquiries, please do not hesitate to contact us.

  <img src="/images/rockfish.png" alt="RockFish Cluster Image">

  

 
    This project is supported by grant #BIO230096 from the XSEDE National Center for Supercomputing.
 


