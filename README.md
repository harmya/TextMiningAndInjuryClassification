# Project: Text Mining and Classification of Injury Narratives

Research Group: Intelligent Decision Support Systems (INDESS) </br>
Mentor : Professor Gaurav Nanda </br>
Last Project Update : December 2022 </br> 
Work Presented at: Summer 2023 Research Expo at Purdue, UR Research Conference Fall 2022.

## **Summary for Investigating Explainability of Machine Learning Model Decisions for Injury Surveillance:**
Injury Surveillance in the public health sector is done by humans based on accident narratives in hospitals. This project aims at using machine learning and natural language processing approaches to identify parts of the narratives that are the most responsible for the ML model decisions by using methodologies in Explainable Artificial Intelligence (XAI)to generate explanations for the ML model decisions at the global (for the entire dataset) and local (for a particular narrative) levels.
We used two frameworks to generate explanations for the current safety dataset. Explainable feature sets are identified using methodologies like: LIME (Local Interpretable Model-Agnostic Explanations), SHAP (SHapley Additive exPlanations) and Integrated Gradients. We consider the most important features for the entire model as well as those which are important for individual instances. The analysis of individual cases gains even more importance when the predictions are incorrect as such an assessment may lead to models with better predictive capabilities.
LIME is used for generating the analysis of the most weighted features, while SHAP is used for generating a dependence plot on the features of the entire model. However, the review of explanations is humanly reviewed to quantify the quality of the explanations generated. We identified that these techniques have additional computational costs, meaning running the explanation multiple times which means the user will have a bigger delay in generating the explanation.

## **Summary for Text Mining and Classification of Injury Narratives:**
In injury surveillance, different aspects of an injury event are captured using injury codes. This task is usually done by human coders and then the data is used for statistical analysis. This project aims to identify various elements of injury surveillance like cause of injury, product involved, nature of injury and so on from the textual narrative of the injury using machine learning and natural language processing approaches.

Human coded data is usually assigned from hospital logs of injury description. It takes months for the data to be available for statistical analysis. This time gap is substantial and many injuries can be prevented if we know about the features of injuries like cause, product involved and nature of injury sooner. Moreover, injuries that are not treated by the hospitals are never logged but can be found as textual narratives in the form of reviews online. This is useful for assimilating more data and making accurate decisions. Hence, by using machine learning and natural language processing, we aim to solve the aforementioned problems which contribute to Global Health by borrowing the frameworks of computer science.

The research process can be broadly classified into three parts: getting data, applying machine learning techniques, concluding the output.
The main purpose of this research is to contribute to Global Health, hence the data and conclusions fall under it, and the process by which we make these conclusions falls under the domain of computer science. The framework used to process all data and derive conclusions uses machine learning and natural language processing techniques.
By having a clear vision about the purpose of this research, a balance is maintained as only the process and the methodology is borrowed from computer science, the data and conclusions are consistent within the domain of global health.

There are a few limitations of using machine learning to classify injury narratives. Firstly, the data is not ubiquitous. Data about certain products cannot be found in textual narratives. Moreover, textual narratives are susceptible to ambiguity in phrasing, choice of words and sarcasm which causes machine learning models to lose accuracy.
To improve the efficacy of models, substantial manual coding can be required. It is difficult for an algorithm on its own to be able to assign classifications in all categories with the same level of confidence and very difficult to improve the accuracy of computer-generated codes for the small categories.

## **Abstract for Purdue Summer Research Expo:**

Aim: Human coded data is usually assigned from hospital logs of injury description. It takes months for the data to be available for statistical analysis. This time gap is substantial and many injuries can be prevented if we know about the features of injuries like cause, product involved and nature of injury sooner. Moreover, injuries that are not treated by the hospitals are never logged but can be found as textual narratives in the form of reviews online. 
Hence, by using machine learning and natural language processing, we aim to solve the aforementioned problems which contribute to Global Health by borrowing the frameworks of computer science.

Methodology: 
Set up Data Pipelines using web scraping frameworks to create datasets of social media data from websites like Amazon, Reddit and Twitter related to product usage and reviews. Developed Natural Language Processing (NLP) Models to identify injury cases, categorize body parts and diagnosis of the injury cases, and safety issues of products.

Results: We had significant results with a working end to end framework. Models averaged an accuracy of ~75% for predictions on scraped datasets. The One-Vs-Rest model worked with precision (~90) to identify the body part injured and the diagnosis in a case from a textual description. Presented the research at Purdue’s Summer Research Symposium and we are currently writing a technical paper.

## **Poster for UR Fall Research Conference:**
![Alt text](poster.png)
