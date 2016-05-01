install_name_tool -change /usr/local/opt/qscintilla2/lib/python2.7/site-packages/PyQt4/libQsci.dylib @rpath/Deps/libQsci.dylib ./PyQt4/Qsci.so
install_name_tool -change /usr/local/Cellar/qscintilla2/2.8.4/lib/libqscintilla2.11.dylib @rpath/Deps/libqscintilla2.11.dylib ./PyQt4/Qsci.so
install_name_tool -change /usr/local/opt/qt/lib/QtGui.framework/Versions/4/QtGui @rpath/Deps/QtGui ./PyQt4/Qsci.so
install_name_tool -change /usr/local/opt/qt/lib/QtCore.framework/Versions/4/QtCore @rpath/Deps/QtCore ./PyQt4/Qsci.so
install_name_tool -change /usr/lib/libc++.1.dylib @rpath/Deps/libc++.1.dylib ./PyQt4/Qsci.so
install_name_tool -change /usr/lib/libSystem.B.dylib @rpath/Deps/libSystem.B.dylib ./PyQt4/Qsci.so
