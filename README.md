<div align="center">
    
# (python)基于neo4j的简单QA系统,和水文预测系统.
</div>
-------------------------------------------------------- 

### 项目文件和代码统计:  
![屏幕截图 2024-02-17 182144](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/9e590d97-bf18-4f81-8314-c6e85d5e8f62)
====================================================================================================================================================
`项目实现详情(避免泄露,项目数据已做删减处理):`  
### 一.搭建neo4j数据库.  
####  1.1 数据库节点:  
![WPS图片(1)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/e833e531-aa00-438a-a465-5d4c5e8280a5)  
####  1.2 数据库效果:  
![WPS图片(1)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/89a4afa0-68ab-4418-9c21-d49a644070c3)  
    
### 二.实现简单QA系统.  
####  2.1 技术实现基础  
  前端:以 html5+css制作网页,js实现网页的动态操作和数据请求。  
  后端:flask搭建本地服务器实现前端数据处理和请求响应，并接入  neo4j。  
####  2.2 QA模型原理  
  基于知识图谱的关键词搜索问答系统，给出相应的街道信息，即可获得与其相关的其他建筑的信息.  
#### 2.3 效果展示  
![WPS图片(2)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/2528bec4-ab95-4f3c-9da2-c7331167efe1)  
![WPS图片(1)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/82e223a9-469d-460f-bdf2-e28c5d23215d)  
  
### 三.实现水文预测系统.  
####  3.1. 水文预测原理:  
  根据已有的降雨和水质数据,假设已知未来某一天或一段时间的降雨数据,即可得到预测的相应的未来水质数据.    
####  3.2. 技术实现基础:  
  前端:以 html5+css制作网页,js实现网页的动态操作和数据请求。  
  后端:flask搭建本地服务器实现前端数据处理和请求响应，并接入neo4j。  
  以本机作为服务器，将后端的数据库，代码程序运行，以供前端的页面调用，前端可控
制训练模型的具体参数，并进行结果的输出。   
####  3.3. 数据分为两类:  
      降雨数据和水质数据.降雨数据包含当天的降雨量,而水质数据则是选取了水中重要的四个评价指标 codcr(化学需氧量),nh3n(氨氮),dox(溶解氧),tp(总磷)作为参考。  
####  3.4. 数据处理办法:  
      借用深度学习工具(长短期记忆网络 lstm(Long Short-Term Memory)),根据已有数据（json、csv 格式）,去训练而得到一个水质的
预测模型。由这个模型我们可以得出降雨和水质的周期性关系。  
####  3.5 训练效果展示  
  ![WPS图片(2)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/75b2d6b1-dd7f-4b6d-a8fd-eec578a2b8fb)  
####  3.6 效果展示  
![WPS图片(1)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/49fdc158-320c-4395-973b-c60c65df7e31)  
![WPS图片(2)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/221417dd-471e-45d6-a3e1-f3190d2d068c)  
  3.6  预测值与真实值展示  
![WPS图片(1)](https://github.com/NaNbNa/DeepLearning_project/assets/144761706/6081a138-8308-4643-981b-6dff19ae3053)  
  



  
  

