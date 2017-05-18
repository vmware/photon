#java rpm macros
%_java_exports        /etc/profile.d/java-exports.sh
%_java_home %( [[ -f "%{_java_exports}" ]] && echo `cat "%{_java_exports}" | grep -m1 JAVA_HOME | cut -d'=' -f2` )
#ant
%_ant_exports        /etc/profile.d/apache-ant.sh
%_ant_home %( [[ -f "%{_ant_exports}" ]] && echo `cat "%{_ant_exports}" | grep -m1 ANT_HOME | cut -d'=' -f2` )
#maven
%_maven_exports        /etc/profile.d/apache-maven.sh
%_maven_home %( [[ -f "%{_maven_exports}" ]] && echo `cat "%{_maven_exports}" | grep -m1 MAVEN_HOME | cut -d'=' -f2` )
