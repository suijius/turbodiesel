3. Точки зрения
===============

3.1 Функциональная
------------------

+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Определение           | Описывает функциональные элементы времени выполнения их свойства, интерфейсы и основные взаимодействия          |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Аспекты               | Функциональные возможности, Внешние интерфейсы, Внутренняя структура, Философия дизайна                         |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Модели                | Functional structure model                                                                                      |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Проблемы и ловушки    | Плохо определенные интерфейсы, плохо изучены обязанности, инфраструктура моделируется как функциональных        |
|                       | элементов, перегружены вид, диаграммы без определений элементов, трудности в согласовании потребностей кратного |
|                       | заинтересованные стороны, недостаточный уровень детализации, «Бог элементов", и слишком много зависимостей      |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Заинтересованные лица | Все                                                                                                             |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+
| Применение            | Везде                                                                                                           |
+-----------------------+-----------------------------------------------------------------------------------------------------------------+

3.1.1 Обзор
+++++++++++

Функциональное представление системы определяет архитектурные элементы, которые обеспечивают функциональность системы.
Представление описывает функциональную структуру системы, в том числе ключевых функциональных элементов, их ответственности, интерфейсов они выставляют,
и взаимодействия между ними. Взятые вместе, это демонстрирует, как система будет выполнять функции, требуемые от него.
Функциональная вид является краеугольным камнем большинства объявления и часто первая часть описания, что заинтересованные стороны пытаются читать.
(Слишком часто, это также единственный вид архитектуры произведенного.) Это, пожалуй, самый простой вид для заинтересованных сторон, чтобы понять.
Функциональная вид обычно приводит определение других архитектурных просмотров (информационных, параллелизм, разработка, внедрение, и оперативных).
Вы почти всегда создать функциональный вид и часто проводите большую часть своего времени, определяющая и уточнения его.

Как и во всех других мнений, задача при определении функционального вид является включение соответствующего уровня детализации.
Фокус на том, что архитектурном отношении, другими словами, то, что имеет заметное влияние на заинтересованных сторон-а остальное в ваших дизайнеров.

3.1.2 Аспекты
+++++++++++++

Functional Capabilities
***********************

Функциональные возможности определить, что требуется система делать-и, явно или неявно, что это не требуется сделать
(либо потому, что эта функциональность выходит за рамки рассмотрения или потому что это предусмотрено в другом месте).
На некоторых проектов, вам будет предоставлена ​​утвержденный техническое задание в начале определения архитектуры,
и вы можете сосредоточиться на функциональной точки зрения на показ, как ваши архитектурные элементы работают вместе,
чтобы обеспечить эту функциональность. Если вы не дали техническое задание хорошего качества, ответственность падает на вас,
прежде чем продолжить дальше, чтобы документ и получить согласие на высоком уровне о том, что система должна делать.

External Interfaces
*******************

Внешние интерфейсы являются потоки данных и управления между системой и другие.
Данные могут поступать внутрь (как правило, в результате чего внутренний изменения состояния системы) и / или наружу (как правило, в результате внутренних изменений состояния системы).
Поток управления может быть входящий (запрос внешней системой в вашей выполнить задачу) или исходящий (просьбу систему на другую, чтобы выполнять определенную задачу).
Определения интерфейсов нужно учитывать как синтаксис интерфейса (структура данных или запросу) и семантику (его значение или эффект).

Internal Structure
******************

В большинстве случаев, вы можете спроектировать систему в ряде различных способов удовлетворения своих потребностей.
Она может быть построена как единый монолитный лица или коллекции слабосвязанных компонентов; она может быть построена из ряда
стандартных пакетов, связанных между собой с помощью товарной промежуточного, или написанный с нуля; его
функциональные потребности даже могут быть удовлетворены веб-услуг, обеспечиваемых системами внешних по отношению к организации.
Внутренняя структура системы определяется ее внутренними элементами, что они делают (то есть, как они отображением на требованиях),
и как они взаимодействуют друг с другом. Это внутренняя организация может иметь большое влияние на свойства качества этой системы,
таких как его доступность, отказоустойчивость возможностью масштабирования и безопасности (например, сложная система, как правило,
сложнее обеспечить, чем простой одного).

Design Philosophy
*****************

Many of your stakeholders will be interested only in what the system does
and the interfaces it presents to users and to other systems. Other stakeholders will be interested in how well the architecture adheres to sound principles
of design. Technical stakeholders want a sound architecture because a welldesigned system is easier to build, operate, and enhance. Other stakeholders—particularly acquirers—want this because it is faster, cheaper, and easier
to get a well-designed system into production.
The design philosophy will be underpinned by a number of design qualities such as those listed in Table 16–1.

TABLE 16–1 DESIGN QUALITIES

+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Design               |                                                                          |                                                               |
| Quality              | Description                                                              |         Significance                                          |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Separation           | To what extent is each internal element responsible for a distinct part  | High separation results in a system that is easier to build,  |
| of concerns          | of the system’s operation? To what extent is common processing performed | support, and enhance but may adversely impact performance and |
|                      | in only one place?                                                       | scalability compared with a monolithic approach.              |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Cohesion             | To what extent are the functions provided by an element strongly related | High cohesion is logically sensible and tends to result in    |
|                      | to each other?                                                           | simpler, less error-prone designs.                            |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Coupling             | How strong are the element interrelationships? To what extent do changes | Loosely coupled systems are often easier to build, support,   |
|                      | in one module affect others?                                             | and enhance but may suffer from poor scalability compared     |
|                      |                                                                          | with a monolithic approach.                                   |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Volume               | What proportion of processing steps involve interactions between         | Communicating between certain types of elements can be an     |
| of element           | elements as opposed to within an element?                                | order of magnitude more expensive (in terms of processing     |
| interactions         |                                                                          | time and elapsed time), and significantly less reliable,      |
|                      |                                                                          | than performing an operation within a functional element.     |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Functional           | How amenable is the system to supporting functional changes?             | Systems that are designed to be easy to change are usually    |
| flexibility          |                                                                          | harder to build and typically don’t perform as well as        |
|                      |                                                                          | systems that are less adaptable.                              |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+
| Overall              | Does the architecture “look right” when decomposed into elements?        | If the architecture doesn’t look right, this may indicate     |
| coherence            |                                                                          | underlying problems and may also make it harder for           |
|                      |                                                                          | stakeholders to understand.                                   |
+----------------------+--------------------------------------------------------------------------+---------------------------------------------------------------+

3.1.3 Типы моделей
++++++++++++++++++

Functional Structure Models
***************************

The functional structure model typically contains the following elements.

- Functional elements: A functional element is a well-defined part of the runtime system that has particular responsibilities and exposes well-defined interfaces that allow it to be connected to other elements. At its simplest level, an element is a software code module, but in other contexts it
  could be an application package, a data store, or even a complete system. In general, it is not appropriate to model underlying infrastructure as
  functional elements, unless that infrastructure performs a functionally significant task, independent of the other functional elements. Infrastructure that simply supports the operation of the functional elements
  should normally not be shown in the Functional view; it is best considered in the Deployment view.
- Interfaces: An interface is a well-defined mechanism by which the functions of an element can be accessed by other elements. An interface is defined by the inputs, outputs, and semantics of each operation offered
  and the nature of the interaction needed to invoke the operation.
- Connectors: Connectors are the pieces of your architecture that link the elements together to allow them to interact. A connector defines the interaction between the elements that use it and allows the nature of the
  interaction to be considered separately from the semantics of the operation being invoked. The nature of the interactions between elements can be intimately bound up in how they are connected.
  The amount of consideration you need to give connectors depends on your circumstances. At one extreme, you can just note that one element
  connects to another. At the other extreme, a connector can be modeled as a type of element in its own right. As always, focus here on what is architecturally significant.
- External entities: External entities can represent other systems, software programs, hardware devices, or any other entity that your system communicates with. They are obtained from your system context definition,
  and each appears in the functional model at the far end of an interface.

The functional structure model does not contain entities like processes or
threads that define how code is packaged and executed. Therefore, the Functional view does not constrain how the functional components are packaged
to allow their deployment and execution—this is the domain of the Concurrency view.




