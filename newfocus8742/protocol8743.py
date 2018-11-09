from .protocol import NewFocus8742Protocol, _make_do, _make_ask

def conv_int_tuple(s):
    return tuple(map(int, s.split(",")))

class NewFocus8743Protocol(NewFocus8742Protocol):
    """New Focus/Newport 8743 Driver.

    Two Channel Closed loop Picomotor controller and driver module, Closed-Loop, 2 Channel
    https://www.newport.com/p/8743-CL
    """

    set_absolute_position_search_mode = _make_do("AD",
            """Absolute position search mode set.
            
            This command is used to set the absolute position search mode for an axis. It is used to specify the final
            move the controller should make after determining the absolute position of the stage/positioner. If this
            command is issued when an axis’ absolute position search is in progress, the controller will generate
            “COMMAND NOT ALLOWED DURING HOMING” error message.
            
            Arguments
            xx 1 to 2  Axis number
            nn 0 (Default) Do not make any further moves after finding absolute position
               1 Move to the position at the start of absolute position search
               2 Move to absolute zero position """)

    get_absolute_position_search_mode = _make_ask("AD?",
            """Absolute position search state query.                                  
                               
            This command is used to query the state of absolute position search process for an axis.""")

    set_absolute_encoder_parameters = _make_do("AE",
            """Quasi-absolute encoder parameters set.
            
            This command is used to set the quasi-absolute encoder parameters for an axis. Since these values are 
            stage/positioner-specific, please consult the stage’s user’s manual for guidance on correct parameter 
            values. If this command is issued when an axis’ absolute position search is in progress, the controller 
            will generate “COMMAND NOT ALLOWED DURING HOMING” error message.
            
            Argument Value Description
            xx 1 to 2 Axis number
            nn1 570 (Default) Start index increment
            nn2 8190 (Default) Start absolute position
            nn3 10 (Default) Index increment
            nn4 25 (Default) Maximum number of index marks
            """)

    get_absolute_encoder_parameters = _make_ask("AE?",
            """Quasi-absolute encoder parameters query.
            
            This command is used to query the quasi-absolute encoder parameters for an axis
            """, conv_int_tuple)

    start_absolute_position_search = _make_do("AF",
            """Start absolute position search.
            
            This command is used to start the absolute position search process for an axis. If this command is 
            issued when an axis’ motion is in progress, the controller will generate “MOTION IN PROGRESS” error message. 
            If this command is issued before telling the controller that a quasi-absolute encoder is connected and the 
            displacement units are encoder counts, the controller will generate “QUASI-ABSOLUTE ENCODER NOT CONNECTED” 
            error message.
            
            xx 1 to 2 Axis number
            """)

    position_search_done = _make_ask("AF?",
            """Absolute position search state query.
            
            This command is used to query the state of absolute position search process for an axis.
            xx 1 to 2 Axis number
            
            Response Value Description
            Value false Motion in progress (Absolute position search in progress)
                  true  Motion done (Absolute position search completed)""", bool)

    set_update_interval = _make_do("CL",
            """Closed-loop control update interval set.
            
            This command is used to set the closed-loop control update interval for an axis. This will be the time 
            duration between position error corrections during closed-loop positioning. 
            For maximum user application flexibility, each axis is allowed to have a different and independent time 
            interval setting from one another.
            Position error corrections occur only during position regulation (holding position) as opposed to while 
            moving.
            NOTE: Motor positioning units must be in ‘Counts’ (see SN command) and closed-loop mode enabled 
            (see MM command) for CL command setting to take effect.
            
            Argument Value Description
            xx 1 to 2 Axis number
            nn 0.1 to 100000 Update interval (sec). Default = 0.1 sec
            """)

    get_update_interval = _make_ask("CL?",
            """Closed-loop control update interval query.
            
            This command is used to query the closed-loop control update interval for an axis.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value Integer Update interval (sec)
            """)

    set_deadband = _make_do("DB",
            """Deadband set.
            
            This command is used to set the position deadband value for an axis. Since a majority of electro-mechanical
            systems have mechanical backlash or frictional hysteresis, closed-loop positioning can at times lead to
            oscillation or limit cycling of the systems around a desired position. In such situations, setting position 
            deadband value judiciously can avoid limit cycling of the systems.
            Note that this command is effective only during position regulation (holding position) as opposed to while 
            moving. Also, the positioning units must be in ‘Counts’ (see SN command) and closed-loop positioning must
            be enabled (see MM command) for DB command to take effect.
            NOTE: An error will be generated if the controller makes more than 100 consecutive unsuccessful attempts 
            to correct the stage position, but is unable to bring the following error to within specified deadband 
            setting.
            
            Argument
            xx 1 to 2 Axis number
            nn 0 to 2147483647 Deadband value (units). Default = 0""")

    get_deadband = _make_ask("DB?",
            """Deadband query.
            
            This command is used to query the deadband value for an axis.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value Integer Deadband (units)
            """)

    set_following_error_limit = _make_do("FE",
            """Maximum following error threshold set.
            
            This command is used to set the maximum allowed following (tracking) error threshold for an axis. This 
            error is defined as the difference between the real (encoder) position and destination (target) position 
            of a motion device. The real position is the one reported by the position sensing device (i.e., quadrature 
            encoder).
            If following error checking is enabled (see ZH command) and the following error exceeds the maximum 
            threshold specified with this command, the controller will automatically disable closed-loop positioning 
            (see MM command). Also, the positioning units must be set to ‘Counts’ in order for following error tracking 
            and closed-loop correction to take effect (see SN command).
            NOTE: Following error checking must be enabled (see ZH command) in order for FE command to take effect.
            
            Argument Value Description
            xx 1 to 2 Axis number
            nn 0 to 2147483647 Following error value (units). Default = 1000""")

    get_following_error_limit = _make_ask("FE?",
            """Maximum following error threshold query.
            
            This command is used to query the following error threshold value for an axis.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value Integer Following error (units)""")

    enable_closed_loop = _make_do("MM",
            """Enable/disable closed-loop positioning.
            
            This command is used to enable/disable closed-loop positioning of an axis. If closed-loop positioning is 
            disabled, Picomotors can be commanded to move, but the controller will not perform any end of move position
            correction. Closed-Loop correction takes affect only during position regulation (holding position) as 
            opposed to while moving. Furthermore, the positioning units must be in ‘Counts’ (see SN command)

            NOTE: Closed-Loop correction is automatically disabled (MM=0) after a controller reset, power-up, or a 
            Following Error condition (see FE command).
            Argument Value Description
            xx 1 to 2 Axis number
            nn 0 Disable closed-loop positioning. Default = 0
            1 Enable closed-loop positioning
            """)

    closed_loop_status = _make_ask("MM?",
            """Closed-loop positioning status query.
            
            This command is used to query the closed-loop positioning status for an axis.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value 0 or 1 Disable or Enable
            """, bool)

    find_travel_limit = _make_do("MT",
            """Find hardware travel limit.
            
            This command is used to move an axis to its limit (positive or negative). The controller will automatically
            stop the axis after crossing the travel limit. If this command is issued when an axis’ motion is in 
            progress, the controller will ignore this command and generate “MOTION IN PROGRESS” error message.
            The controller executes a unique sequence of motion in order to locate and finally stop the positioner at a 
            repeatable limit position. The repeatability precision depends mostly on the repeatability of the limit 
            switch itself and ability to stop and hold final position. It is not unusual for a Limit signal to be 
            repeatable to within 20 encoder counts (e.g., 8310 and 8310-V actuators).
            Positioners with Limit signals typically have a negative and positive travel limit. Hence, the Find Limit 
            function requires that the user tell the controller which limit (positive or negative) to find so the 
            controller can move in that direction.
            The MT motion status can be monitored using the Motion Done (MD?) command.
            NOTE: The controller will NOT stop motion until it finds the travel limit. Send the Stop (ST) or Abort (AB) 
            motion command to terminate motion.
            NOTE: Travel limit signal checking should first be enabled (see ZH command) before Find Limit (MT) command 
            is issued. Otherwise, error x35 will be generated.
            NOTE: MT is compatible with 8310 and 8310-V positioners as each model outputs travel limit signals. 
            However, MT command is NOT compatible with 8410 rotary stage.
            Argument Value Description
            xx 1 to 2 Axis number
            nn + Travel limit search of desired axis in positive direction
               - Travel limit search desired axis in negative direction
            """)

    get_move_direction = _make_ask("MV?")

    find_index_position = _make_do("MZ",
            """Find nearest index search.
            
            This command is used to move an axis to its nearest Index in positive or negative direction. The controller
            will automatically stop the axis after crossing the index. If this command is issued when an axis’ motion 
            is in progress, the controller will ignore this command and generate “MOTION IN PROGRESS” error message.
            The controller executes a unique sequence of motion in order to locate and finally stop the positioner at 
            a repeatable Index position. The repeatability precision depends mostly on the repeatability of the Index 
            itself and ability to stop and hold final position. It is not unusual for a Find Index function to be 
            repeatable to within 4 encoder counts (e.g., 8410 rotary stage).
            The MZ motion status can be monitored using the Motion Done (MD?) command.
            NOTE: The controller will NOT stop motion until it finds the Index signal transition. Send the Stop (ST) 
            or Abort (AB) motion command to terminate motion.
            NOTE: The Find Index function is compatible with 8410 positioner.
            
            Argument Value Description
            xx 1 to 2 Axis number
            nn + Index search of desired axis in positive direction
            - Index search desired axis in negative direction
            """)

    get_absolute_position_initialized = _make_ask("OF?",
            """Query absolute position found following a reset.
            
            This command is used to query if an axis’ absolute position was found following a reset.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value false Absolute position not found after controller reset
                  true Absolute position found after controller reset
            """, bool)

    find_home = _make_do("OR",
            """Find Home search.
            
            This command is used to execute a home search routine for an axis. The controller will automatically stop 
            the axis after crossing the index. If this command is issued when an axis’ motion is in progress, the 
            controller will ignore this command and generate “MOTION IN PROGRESS” error message.
            The controller executes a unique sequence of motion in order to locate and finally stop the positioner at 
            a repeatable Home position. The repeatability precision depends mostly on the repeatability of the Home 
            switch itself and ability to stop and hold final position. It is not unusual for a Find Home function to be 
            repeatable to within 20 encoder counts (e.g., 8410-V positioner).
            Issue the Define Home (DH) command after OR completed to make Home position the reference for Position 
            Absolute (PA) commands.
            The Home search motion status can be monitored using the Motion Done (MD?) command.
            NOTE: The controller will NOT stop motion until it finds the Home signal transition. Send the Stop (ST) or 
            Abort (AB) motion command to terminate motion.
            NOTE: The Find Home function is compatible with 8310-V positioner.
            NOTE: The Find Home function is NOT compatible with 8310 and 8410 positioners.
            Argument Value Description
            xx 1 to 2 Axis number
            """)

    get_hardware_status = _make_ask("PH?",
            """Hardware status query.
            
            This command is used to query general hardware status for all the axes. This function allows the user to 
            observe the various digital input signals as they appear to the controller in real-time.
            Note that the positioner’s Home or Index signals come in on the same controller differential input pair, 
            feedback connector pins 14 & 15. That means that if an 8410 rotary positioner is connected then the 
            Home/Index input actually represents ‘Index’ signal status, because that is what the 8410 provides. However,
            if an 8310-V actuator is connected then the Home/Index represents ‘Home’ signal status, because that is what
            the 8310-V provides. 
            Note that the Index signal is a momentary signal transition, a few encoder counts wide, whereas a Home 
            signal is typically a logical High from the middle of positioner travel range to the positive travel limit 
            and a logical Low from the negative travel limit to the positioner middle.
            The controller treats the signal differently, as either Home or Index type, depending on whether the OR 
            (Find Home) or MZ (Find Index) command was issued.
            Response Value Description
            nn Integer Decimal representation of binary number
            """)

    set_axis_units = _make_do("SN",
            """Axis displacement units set.
            
            This command is used to set the displacement units of an axis.
            The inherent Picomotor positioner operates in steps and is open-loop. However, when a quadrature encoder 
            is integrated into a Picomotor positioner and those signals are brought to the controller’s feedback 
            connector then it is possible to monitor real position using encoder ‘Counts’. The use of ‘Counts’ as 
            positioning units makes possible closed-loop control. However, when the control is set to use ‘Steps’ as 
            positioning units then only open-loop control is possible.
            NOTE: If units set to ‘Steps’ (SN=0) then only open-loop positioning is possible.
            
            Argument Value Description
            xx 1 to 2 Axis number
            nn 0 Units are steps (open-loop mode).
            1 Units are encoder counts. Default = 1""")

    get_axis_units = _make_ask("SN?",
            """Axis displacement units query.
            
            This command is used to query the displacement units for an axis.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value 0 or 1 Steps or Encoder counts""")

    set_positive_limit = _make_do("SR",
            """Positive software travel limit set.
            
            This command is used to set the positive software travel limit for an axis. If this command is issued when 
            an axis’ absolute position search is in progress, the controller will generate “COMMAND NOT ALLOWED DURING 
            HOMING” error message. The controller will generate “PARAMETER OUT OF RANGE” error message if the value 
            specified is lower than the negative software travel limit. This value can be saved in controller’s 
            non-volatile memory by issuing “SM” command. If define home (DH) command is issued after this command is 
            issued, the controller will adjust the software travel limits and temporarily override the value specified 
            using this command. The temporarily modified software limits are not saved in controller’s non-volatile 
            memory. This allows the controller to preserve user-specified software limits. Bit #3 in hardware 
            configuration register (refer ZH command) must be set to 1 in order for the controller to check for any 
            software travel limit violations.
            Argument Value Description
            xx 1 to 2 Axis number
            nn Integer Positive software travel limit (encoder counts)
            """)

    get_positive_limit = _make_ask("SR?",
            """Positive software travel limit query.
            
            This command is used to query the positive software travel limit for an axis. The response to this command 
            can be different from the value specified using “SR” command if define home (DH) command is issued after 
            “SR” command is issued.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value Integer Positive software travel limit""")

    set_negative_limit = _make_do("SL",
            """Negative software travel limit set.
            
            This command is used to set the negative software travel limit for an axis. If this command is issued when 
            an axis’ absolute position search is in progress, the controller will generate “COMMAND NOT ALLOWED DURING 
            HOMING” error message. The controller will generate “PARAMETER OUT OF RANGE” error message if the value 
            specified is greater than the positive software travel limit. This value can be saved in controller’s 
            non-volatile memory by issuing “SM” command. If define home (DH) command is issued after this command is 
            issued, the controller will adjust the software travel limits and temporarily override the value specified 
            using this command. The temporarily modified software limits are not saved in controller’s non-volatile 
            memory. This allows the controller to preserve user-specified software limits. Bit #3 in hardware 
            configuration register (refer ZH command) must be set to 1 in order for the controller to check for any 
            software travel limit violations.
            Argument Value Description
            xx 1 to 2 Axis number
            nn Integer Negative software travel limit (encoder counts)
            """)

    get_negative_limit = _make_ask("SL?",
            """Negative software travel limit query.
            
            This command is used to query the negative software travel limit for an axis. The response to this command 
            can be different from the value specified using “SL” command if define home (DH) command is issued after 
            “SL” command is issued.
            Argument Value Description
            xx 1 to 2 Axis number
            Response Value Description
            Value Integer Negative software travel limit""")