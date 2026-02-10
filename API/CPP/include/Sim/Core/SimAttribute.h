//////////////////////////////////////////////////////////////////////////////
//
// Copyright 2026 Autodesk, Inc. All rights reserved.
//
// Use of this software is subject to the terms of the Autodesk license
// agreement provided at the time of installation or download, or which
// otherwise accompanies this software.
//
//////////////////////////////////////////////////////////////////////////////

#pragma once
#include "../../Core/Base.h"
#include "../SimTypeDefs.h"
#include <string>
#include <vector>

// THIS CLASS WILL BE VISIBLE TO AN API CLIENT.
// THIS HEADER FILE WILL BE GENERATED FROM NIDL.
#include "../../Core/OSMacros.h"

#ifdef SIMXINTERFACE_EXPORTS
# ifdef __COMPILING_ADSK_SIM_SIMATTRIBUTE_CPP__
# define ADSK_SIM_SIMATTRIBUTE_API XI_EXPORT
# else
# define ADSK_SIM_SIMATTRIBUTE_API
# endif
#else
# define ADSK_SIM_SIMATTRIBUTE_API XI_IMPORT
#endif

namespace adsk { namespace sim {

/// !!!!! Warning !!!!!
/// ! This is hidden and not officially supported
/// !!!!! Warning !!!!!
/// 
/// Object that represents a SimAttribute.
class SimAttribute : public core::Base {
public:

    /// The name of the SimAttribute as displayed in the browser.
    std::string name() const;
    bool name(const std::string& value);

    /// The input entities. The collection can contain vertices, edges, faces, bodies, etc.
    /// All of the entities must be of a single type. For example, it can't contain vertices and faces
    /// but only vertices or faces.
    std::vector<core::Ptr<core::Base>> entities() const;

    ADSK_SIM_SIMATTRIBUTE_API static const char* classType();
    ADSK_SIM_SIMATTRIBUTE_API const char* objectType() const override;
    ADSK_SIM_SIMATTRIBUTE_API void* queryInterface(const char* id) const override;
    ADSK_SIM_SIMATTRIBUTE_API static const char* interfaceId() { return classType(); }

private:

    // Raw interface
    virtual char* name_raw() const = 0;
    virtual bool name_raw(const char* value) = 0;
    virtual core::Base** entities_raw(size_t& return_size) const = 0;
    virtual void placeholderSimAttribute0() {}
    virtual void placeholderSimAttribute1() {}
    virtual void placeholderSimAttribute2() {}
    virtual void placeholderSimAttribute3() {}
    virtual void placeholderSimAttribute4() {}
    virtual void placeholderSimAttribute5() {}
    virtual void placeholderSimAttribute6() {}
    virtual void placeholderSimAttribute7() {}
    virtual void placeholderSimAttribute8() {}
    virtual void placeholderSimAttribute9() {}
    virtual void placeholderSimAttribute10() {}
    virtual void placeholderSimAttribute11() {}
    virtual void placeholderSimAttribute12() {}
};

// Inline wrappers

inline std::string SimAttribute::name() const
{
    std::string res;

    char* p= name_raw();
    if (p)
    {
        res = p;
        core::DeallocateArray(p);
    }
    return res;
}

inline bool SimAttribute::name(const std::string& value)
{
    return name_raw(value.c_str());
}

inline std::vector<core::Ptr<core::Base>> SimAttribute::entities() const
{
    std::vector<core::Ptr<core::Base>> res;
    size_t s;

    core::Base** p= entities_raw(s);
    if(p)
    {
        res.assign(p, p+s);
        core::DeallocateArray(p);
    }
    return res;
}
}// namespace sim
}// namespace adsk

#undef ADSK_SIM_SIMATTRIBUTE_API