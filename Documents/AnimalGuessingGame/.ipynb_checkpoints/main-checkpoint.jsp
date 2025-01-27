<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" prefix = "c"%>


<html>
<head> 
    <title>Question 2</title> 
</head>
<body>
	<c:forEach animal="${animal.getanimalID}" var="animalID">
    <p>Is the animal a  <a id="yes">yes</a><a id="no">no</a></p>
    <c:if ${param.id}="yes">
    <c:redirect url="main.jsp/class"></c:redirect></c:if></c:forEach>
    <c:forEach animal="${animal.getclassID}" var="classID">
    <p>Is the animal a  <a id="yes">yes</a><a id="no">no</a></p>
    <c:if ${param.id}="yes">
    <c:redirect url="main.jsp/order"></c:redirect></c:if></c:forEach>
    <c:forEach animal="${animal.getorderID}" var="orderID">
    <p>Is the animal a  <a id="yes">yes</a><a id="no">no</a></p>
    <c:if ${param.id}="yes">
    <c:redirect url="main.jsp/species"></c:redirect></c:if></c:forEach>
    <c:forEach animal="${animal.getspeciesID}" var="speciesID">
    <p>Is the animal a  <a id="yes">yes</a><a id="no">no</a></p>
    <c:if ${param.id}="yes">
    <c:redirect url="Iwin.html"></c:redirect></c:if></c:forEach>
    
</body>
</html>