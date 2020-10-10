Change log
================================================================================

0.6.0 - 10.10.2020
--------------------------------------------------------------------------------

**Updated**

#. New style xlsx plugins, promoted by pyexcel-io v0.6.2.

0.5.2 - 23.10.2017
--------------------------------------------------------------------------------

**updated**

#. `pyexcel#105 <https://github.com/pyexcel/pyexcel/issues/105>`_, remove gease
   from setup_requires, introduced by 0.5.1.
#. remove python2.6 test support
#. update its dependecy on pyexcel-io to 0.5.3

0.5.1 - 20.10.2017
--------------------------------------------------------------------------------

**added**

#. `pyexcel#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include
   LICENSE file in MANIFEST.in, meaning LICENSE file will appear in the released
   tar ball.

0.5.0 - 30.08.2017
--------------------------------------------------------------------------------

**Updated**

#. put dependency on pyexcel-io 0.5.0, which uses cStringIO instead of StringIO.
   Hence, there will be performance boost in handling files in memory.

**Relocated**

#. All ods type conversion code lives in pyexcel_io.service module
#. `#4 <https://github.com/pyexcel/pyexcel-odsr/issues/4>`_, handle unseekable
   stream given by http response.

0.4.3 - 25.08.2017
--------------------------------------------------------------------------------

**Relocated**

#. All ods type conversion code lives in pyexcel_io.service module
#. `#4 <https://github.com/pyexcel/pyexcel-odsr/issues/4>`_, handle unseekable
   stream given by http response.

0.4.2 - 20.08.2017
--------------------------------------------------------------------------------

0.4.1 - 26.07.2017
--------------------------------------------------------------------------------

**Updated**

#. PR `#3 <https://github.com/pyexcel/pyexcel-odsr/pull/3>`_, support fods, flat
   ods file

0.4.0 - 19.06.2017
--------------------------------------------------------------------------------

**Updated**

#. Updated to use lml interface

0.3.2 - 07.05.2017
--------------------------------------------------------------------------------

**Updated**

#. issue `#2 <https://github.com/pyexcel/pyexcel-odsr/issues/2>`_, not all texts
   in a multi-node cell were extracted.

0.3.1 - 13.04.2017
--------------------------------------------------------------------------------

**Updated**

#. issue `#1 <https://github.com/pyexcel/pyexcel-odsr/issues/1>`_, PT288H00M00S
   is valid duration
#. initial release. It has all functionalities of pyexcel-ods and pyexcel-ods3.
   Specially, it supports partial reading of the ods file. When dealing with big
   data file, this capability enables pagination feature to indeed read partial
   files.

0.3.0 - 02.02.2017
--------------------------------------------------------------------------------

**Updated**

#. issue `#1 <https://github.com/pyexcel/pyexcel-odsr/issues/1>`_, PT288H00M00S
   is valid duration
#. initial release. It has all functionalities of pyexcel-ods and pyexcel-ods3.
   Specially, it supports partial reading of the ods file. When dealing with big
   data file, this capability enables pagination feature to indeed read partial
   files.
