<h1 align="center">OVN Repository</h1>
<h3 align="left">Description</h3>
A repository for OVN exams and labs. The Final version is in LabFinal. <br>
The main class is the<b> Network Class</b>. <br>

The project was used to present a virtualization of a nodal network architecture.
It represents a virtual simulation between the physical and network layer for networking. 
<ul>
  <li>We had to emulate a fiber network, such that it was able to simulate traffic through the network and based on the concepts of SNR and latency, we had to search for an optimized pathing through the network. </li>
  <li>The network itself is a partly disaggregated network.</li>
  <li>We deal with a software abstraction of an actual network, represented by a JSON file, which was unique to each student. </li>
</ul>
<h3 align="left">Object Oriented Programming</h3>
Python is the main OOP language used in order to build the paradigm between the layers previously mentioned. 
Along with it, various libraries are used. These include: <b>Pandas</b>, <b>NumPy</b>, and <b>MatPlotlib</b> for the visualizations including net rate analysis between different nodes and different routes within the architecture, as well as mapping the impact of the varying bitrates. 
We used different mathematical models to simulate and represent the network elements and subsystems, for example the amplifiers installed along the route. 
<ol>
  <li>The Network: <p>The network assigned to me consisted of 5 nodes, where each node was connected by multimodal fiber lines.</p></li>
  <li>Signal: We use attributes to define a signal propagating through the network. These attributes can include <ul><li>Signal Power</li> <li>Noise Power</li><li>Latency</li></ul></li>
  A LightPath will be a transparent route over the network at a given wavelength.
  <li>Node Class: represents the nodes or switch in the OTN network, able to add/drop local traffic.</li>
  <li>Line class: The line or optical fiber between two nodes, with each line having 10 channels each to allow for different frequency slots</li>
</ol>
![image](https://github.com/troopermsk/OVNRepo/assets/118739430/228590d5-851a-4939-96c8-c3d0556341b5)

![image](https://github.com/troopermsk/OVNRepo/assets/118739430/2a82ac4a-0d08-4d87-9c0b-ded5782a9339)

![image](https://github.com/troopermsk/OVNRepo/assets/118739430/be85e78a-8a43-465f-9b14-02cf2a48fd59)

![image](https://github.com/troopermsk/OVNRepo/assets/118739430/c8724c12-ad09-419e-9766-309283cc31cc)

![image](https://github.com/troopermsk/OVNRepo/assets/118739430/14ae4439-758d-4c5a-a376-ec241ddd92a7)
